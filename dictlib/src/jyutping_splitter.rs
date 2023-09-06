use std::str::{Chars, CharIndices};

pub struct JyutpingSplitter<'a>
{
    inner : &'a str,
    current : usize,
    char_iter : CharIndices<'a>,
}

impl<'a> JyutpingSplitter<'a>
{
    pub fn new(s : &'a str) -> Self {
        Self {
            inner: s,
            current: 0,
            char_iter: s.char_indices(),
        }
    }
}

impl<'a> Iterator for JyutpingSplitter<'a>
{
    type Item = &'a str;
    fn next(&mut self) -> Option<Self::Item>
    {
        let mut start = self.current;
        while let Some((i, x)) = self.char_iter.next()
        {
            if (!x.is_ascii() || x.is_ascii_whitespace() || x.is_ascii_punctuation())
            {
                // Reset, goto next
                start = i + x.len_utf8();
                continue;
            }

            if (x.is_ascii_digit() && i > start)
            {
                let str = &self.inner[start..=i];
                self.current = i + x.len_utf8();
                return Some(str);
            }
        }

        None
    }
}

#[cfg(test)]
mod tests
{
    use super::JyutpingSplitter;

    #[test]
    pub fn test_jyutping_splitter_basic()
    {
        let str = "hello ngo5 hai6 dan dan";
        let mut iter = JyutpingSplitter::new(str);
        assert_eq!(Some("ngo5"), iter.next());
        assert_eq!(Some("hai6"), iter.next());
        assert_eq!(None, iter.next());
    }

    #[test]
    pub fn non_ascii_punct()
    {
        let str = "bat1 daa2 ，soeng6 fong4";
        let mut iter = JyutpingSplitter::new(str);
        assert_eq!(Some("bat1"), iter.next());
        assert_eq!(Some("daa2"), iter.next());
        assert_eq!(Some("soeng6"), iter.next());
        assert_eq!(Some("fong4"), iter.next());
        assert_eq!(None, iter.next());
    }

    #[test]
    pub fn non_ascii_chars()
    {
        let str = "man4 zuk6ＬＯＯＫ";
        let mut iter = JyutpingSplitter::new(str);
        assert_eq!(Some("man4"), iter.next());
        assert_eq!(Some("zuk6"), iter.next());
        assert_eq!(None, iter.next());
    }
}