use std::collections::BinaryHeap;

use crate::compiled_dictionary::*;
use crate::search::*;
use crate::string_search::string_indexof_linear_ignorecase;


impl CompiledDictionary {
    pub fn get_jyutping_matched_spans(&self, entry: &CompiledDictionaryEntry, query_terms: &QueryTerms) -> Vec<(usize, usize)> {
        let mut spans = Vec::new();
        let mut start: usize = 0;

        if let Some(best_match) = get_jyutping_best_match(entry, query_terms) {
            for (i, entry_jyutping) in entry.jyutping.iter().enumerate() {
                let target_string = self.jyutping_store.get_string(*entry_jyutping);

                for (j, x) in best_match.inner.iter().enumerate() {
                    if (x.target_index != i as u32) {
                        continue;
                    }

                    let query_term = &query_terms.jyutping_terms[j];
                    let query_string = query_term.string_with_tone();

                    if let Some(idx) = string_indexof_linear_ignorecase(&query_string, target_string.as_bytes()) {
                        spans.push((start + idx, start + idx + query_string.len()));
                    }
                    else if let Some(t) = query_term.tone && t == entry_jyutping.tone {
                        // Ok that didn't work, try and split non-tone part and tone part and get something
                        let q = &query_term.string_no_tone;
                        if let Some(idx) = string_indexof_linear_ignorecase(q, target_string.as_bytes()) {
                            spans.push((start + idx, start + idx + q.len()));
                        }

                        // At least highlight the tone
                        spans.push((start + target_string.len() - 1, start + target_string.len()));
                    }
                }

                start += target_string.len();
                start += 1;
            }
        }
        else {
            // We shouldnt really get here ever
            debug_assert!(false);
        }

        spans
    }

    pub fn get_english_matched_spans(&self, entry: &CompiledDictionaryEntry, query: &str) -> Vec<(usize, usize)> {
        let mut spans = Vec::new();

        if entry.english_start == entry.english_end {
            return spans;
        }

        //let first_start = self.english_data_starts[entry.english_start as usize] as usize;

        for def_idx in entry.english_start..entry.english_end {
            let start = self.english_data_starts[def_idx as usize] as usize;
            let end = if def_idx + 1 < self.english_data_starts.len() as u32 {
                self.english_data_starts[def_idx as usize + 1] as usize
            } else {
                self.english_data.len()
            };
            let def_bytes = &self.english_data[start..end];

            for split in query.split_ascii_whitespace() {
                if let Some(pos) = crate::string_search::string_indexof_linear_ignorecase(split, def_bytes) {
                    //let field_idx = 2 + (def_idx - entry.english_start) as usize;
                    //let pos = pos + first_start;
                    spans.push((start + pos, start + pos + split.len()));
                }
            }
        }

        spans
    }

    pub fn get_traditional_matched_spans(&self, entry: &CompiledDictionaryEntry, query_terms: &QueryTerms) -> Vec<(usize, usize)> {
        let mut spans = Vec::new();

        for (char_idx, char_id) in entry.characters.iter().enumerate() {
            if query_terms.traditional_terms.contains(char_id) {
                spans.push((char_idx, char_idx + 1));
            }
        }

        spans
    }
}

#[derive(Default, Clone)]
pub struct JyutpingMatchPath {
    inner: Vec<JyutpingMatchPathElem>,
}

impl JyutpingMatchPath {
    pub fn with_capacity(cap : usize) -> Self {
        Self {
            inner: Vec::with_capacity(cap)
        }
    }
}

impl JyutpingMatchPath {
    pub fn contains_entry_index(&self, entry_index: u32) -> bool {
        for e in &self.inner {
            if (e.target_index == entry_index) {
                return true;
            }
        }

        false
    }

    pub fn cost(&self) -> u32 {
        let mut sum = 0;
        for e in &self.inner {
            sum += e.cost;
        }

        sum
    }
}

impl PartialEq for JyutpingMatchPath {
    fn eq(&self, other: &Self) -> bool {
        self.cost() == other.cost()
    }
}

impl Eq for JyutpingMatchPath {
}

impl PartialOrd for JyutpingMatchPath {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        self.cost().partial_cmp(&other.cost())
    }
}

impl Ord for JyutpingMatchPath {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.cost().cmp(&other.cost())
    }
}

#[derive(Debug, Clone, Copy)]
pub struct JyutpingMatchPathElem {
    target_jyutping: Jyutping,
    target_index: u32,
    cost: u32,
}

pub fn get_jyutping_best_match(entry: &CompiledDictionaryEntry, query_terms: &QueryTerms) -> Option<JyutpingMatchPath> {
    let n = query_terms.jyutping_terms.len();

    let mut queue : BinaryHeap<JyutpingMatchPath> = BinaryHeap::new();
    queue.push(JyutpingMatchPath::with_capacity(n));

    while let Some(x) = queue.pop() {
        debug_assert!(x.inner.len() <= n);
        if (x.inner.len() == n) {
            // Done!
            return Some(x);
        }

        for (i, entry_jyutping) in entry.jyutping.iter().enumerate() {
            if x.contains_entry_index(i as u32) {
                // Already don this one
                continue;
            }

            let query_match = &query_terms.jyutping_terms[x.inner.len()];
            if (!query_match.matches.contains(entry_jyutping.base as usize)) {
                // No match
                continue;
            }

            if let Some(tone) = query_match.tone {
                if (tone != entry_jyutping.tone) {
                    continue;
                }
            }

            let mut term_match_cost = 0;
            for (match_bit, cost) in &query_match.match_bit_to_match_cost {
                if (*match_bit == entry_jyutping.base as i32) {
                    term_match_cost = *cost;
                    break;
                }
            }

            let mut cloned = x.clone();
            cloned.inner.push(JyutpingMatchPathElem {
                target_jyutping: *entry_jyutping,
                target_index: i as u32,
                cost: term_match_cost,
            });

            queue.push(cloned);
        }
    }

    Default::default()
}
