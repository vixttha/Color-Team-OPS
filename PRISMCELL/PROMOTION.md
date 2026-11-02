# From specialist research to product release work

1. Specialist may author findings, tests, reproducible patch suggestions/prototypes **only on its home branch** within existing owner scope.
2. Submit a source-bound handoff to Development HQ via the existing product governance process, when permitted. Include stable IDs, exact current product source SHA, paths, concise diff/patch, test receipts, risk, independent logical audit, known limitations, and an optional INCALL notification.
3. Development HQ Head selects Yellow/other one worker, re-checks current source, selectively integrates/cherry-picks **only safe needed files**, reruns tests at new integration SHA and records independent acceptance. Do not merge entire agent branches: Blue includes an older product tree snapshot while other homes may be based on main.
4. Purple Review HQ may review product-level tradeoffs but cannot silently overwrite the independent Purple workcell; product authority remains with existing Head and owner.
5. Workcell ACCEPTED means workspace task accepted, NOT product release accepted. v0.0.2 remains RELEASE_BLOCKED until separately approved evidence and owner release decision.
