# wp2shell PoC

The first ever poc of the pre-auth timing-based SQL injection PoC for the WordPress REST API batch-route confusion chain ([CVE-2026-63030](https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-ff9f-jf42-662q) + [CVE-2026-60137](https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-fpp7-x2x2-2mjf)); still working on command exec

**Affected:** WordPress 6.9.0–6.9.4 and 7.0.0–7.0.1. Fixed in 6.9.5 and 7.0.2.

```bash
python3 poc.py https://target.example
python3 poc.py https://target.example 'SELECT DATABASE()'
```

**Research:** [Searchlight Cyber](https://slcyber.io/research-center/wp2shell-pre-authentication-rce-in-wordpress-core) · [Aikido](https://www.aikido.dev/blog/unauthenticated-rce-in-wordpress-wp2shell) · [Aikido Intel](https://intel.aikido.dev/cve/AIKIDO-2026-696183) · [WordPress](https://wordpress.org/news/2026/07/wordpress-7-0-2-release/)
