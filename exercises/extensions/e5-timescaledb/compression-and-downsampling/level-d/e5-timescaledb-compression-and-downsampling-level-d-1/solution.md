# Solution

Diagnose the compression policy that silently prevents updates to historical rows that operations actually need to update. The recommendation should separate retention from mutability: keep rows that still receive corrections uncompressed, compress only after the correction window closes, and document how to decompress or route exceptional fixes. End with a different retention posture and the metric that proves the policy is safe.
