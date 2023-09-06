use std::collections::{HashSet, BTreeSet};

use bit_set::BitSet;

use crate::{Dictionary, jyutping_splitter::JyutpingSplitter};

pub struct CompiledDictionary
{
    character_store : CharacterStore,
    jyutping_store : JyutpingStore,
}

impl CompiledDictionary {
    pub fn from_dictionary(dict : &Dictionary) -> Self {
        let mut all_characters : BTreeSet<char> = BTreeSet::new();
        let mut all_jyutping_words : BTreeSet<String> = BTreeSet::new();

        for (characters, jyutping) in dict.trad_to_jyutping.inner.iter() {
            for c in characters.chars() {
                all_characters.insert(c);
            }

            // TODO this needs to be a smarter split
            for mut word in JyutpingSplitter::new(jyutping) {
                if (word.len() > 0 && word.chars().last().unwrap().is_ascii_digit()) {
                    word = &word[0..word.len() - 1];
                }
                all_jyutping_words.insert(word.to_owned());
            }
        }

        let mut all_characters_list : Vec<char> = all_characters.into_iter().collect();
        let mut all_jyutping_words_list : Vec<String> = all_jyutping_words.into_iter().collect();

        let character_store = CharacterStore {
            characters: all_characters_list,
            to_jyutping: vec![],
        };

        let jyutping_store = JyutpingStore {
            base_strings: all_jyutping_words_list,

            jyutpings: vec![],
            to_character: vec![],
        };

        println!("Individual characters {}, Individual jyutping words {}", character_store.characters.len(), jyutping_store.base_strings.len());
        println!("{:#?}", jyutping_store.base_strings);

        Self {
            character_store,
            jyutping_store,
        }
    }
}

impl CompiledDictionary {
    fn get_jyutping_matches(&self, s : &str) -> BitSet
    {
        let mut matches = BitSet::new();

        for (i, jyutping) in self.jyutping_store.jyutpings.iter().enumerate() {
            for jyutping_word in jyutping {
                if self.jyutping_store.matches(*jyutping_word, s, None) {
                    matches.insert(i);
                }
            }
        }

        todo!()
    }
}

struct CharacterStore
{
    characters : Vec<char>,
    to_jyutping : Vec<u16>,
}

struct JyutpingStore
{
    base_strings : Vec<String>,

    // TODO Smallvec
    jyutpings : Vec<Vec<Jyutping>>,
    to_character : Vec<u16>,
}

impl JyutpingStore {
    pub fn matches(&self, jyutping: Jyutping, base : &str, tone : Option<u8>) -> bool {
        if let Some(t) = tone {
            if (jyutping.tone != t) {
                return false;
            }
        }

        let base_str = &self.base_strings[jyutping.base as usize];
        base_str.contains(base)
    }
}

#[derive(Debug, Clone, Copy)]
struct Jyutping
{
    // TODO merge to single u16
    base : u16,
    tone : u8,
}

