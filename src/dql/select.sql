SELECT
    rank, *, highlight({fts_idx}, 0, '<b>', '</b>')
FROM
    {fts_idx}
WHERE
    {fts_idx} MATCH ?
ORDER BY
    bm25({fts_idx})
LIMIT
    ?