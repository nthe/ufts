CREATE TRIGGER IF NOT EXISTS {table}_after_insert
AFTER INSERT ON {table}
BEGIN
    INSERT INTO {fts_idx}(rowid, {cols}) VALUES (new.rowid, {new_cols});
END;
    
CREATE TRIGGER IF NOT EXISTS {table}_after_delete
AFTER DELETE ON {table}
BEGIN
    INSERT INTO {fts_idx}({fts_idx}, rowid, {cols}) VALUES('delete', old.rowid, {old_cols});
END;

CREATE TRIGGER IF NOT EXISTS {table}_after_update
AFTER UPDATE ON {table}
BEGIN
    INSERT INTO {fts_idx}({fts_idx}, rowid, {cols}) VALUES('delete', old.rowid, {old_cols});
    INSERT INTO {fts_idx}(rowid, {cols}) VALUES (new.rowid, {new_cols});
END;