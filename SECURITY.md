# Security boundary

This public repository intentionally excludes API keys/provider secrets, private signing keys, raw private sponsor-response payloads, private source-repository history, live judge-access credentials, and unrelated private project files.

Public receipts contain hashes, counts, bounded status fields, and provider/result metadata needed for reproducibility without embedding credentials.

If a secret is discovered in this repository, treat it as exposed and rotate it at the provider.