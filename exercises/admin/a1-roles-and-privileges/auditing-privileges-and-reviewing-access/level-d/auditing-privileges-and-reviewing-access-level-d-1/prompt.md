# Audit a leaked role audit

## Scenario

A leaked role audit shows direct object grants to `app_api_login`, membership in `saas_break_glass`, and ALL PRIVILEGES on the saas schema. Identify every over-grant and propose the targeted REVOKEs.
