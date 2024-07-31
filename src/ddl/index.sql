CREATE VIRTUAL TABLE IF NOT EXISTS {fts_idx}
USING fts5({cols}, content='{table}', tokenize='trigram case_sensitive 0 remove_diacritics 1');