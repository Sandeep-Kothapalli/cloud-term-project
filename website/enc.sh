sqlcipher database.db
ATTACH DATABASE 'encrypted.db' AS encrypted KEY 'my password';
SELECT sqlcipher_export('encrypted');
DETACH DATABASE encrypted;
