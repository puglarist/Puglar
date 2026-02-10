# Firebase Hosting Pre-Deployment Checklist for Web Apps

Use this checklist before running `firebase deploy`.

## 1) Production-readiness basics

- Confirm you are deploying to the correct Firebase project (`firebase use` and `.firebaserc`).
- Review the [Firebase launch checklist](https://firebase.google.com/support/guides/launch-checklist) for cross-service production best practices.
- Verify environment variables and API keys are set appropriately for production.
- Remove debug/test-only behavior and validate final build settings.

## 2) Hosting configuration and deploy flow

- Validate `firebase.json` rewrites/redirects, headers, and cache behavior.
- Test locally with `firebase emulators:start` or `firebase hosting:channel:deploy` preview channels.
- Deploy with `firebase deploy` (or `firebase deploy --only hosting` when appropriate).
- Smoke test your live URLs (`https://<projectId>.web.app` and `https://<projectId>.firebaseapp.com`).

## 3) Domain and runtime architecture decisions

- Connect and verify a custom domain for production branding.
- Decide whether your app needs static hosting only or dynamic/server-rendered behavior.
- For dynamic content and microservices, use Firebase Hosting with Cloud Functions/Cloud Run integration.
- If evaluating App Hosting, confirm framework/runtime compatibility and build/runtime needs.

## 4) Cost, monitoring, and operational safety

- Set Google Cloud budget alerts before launch.
- Monitor Firebase Usage & billing dashboards regularly (overall + Hosting-specific usage).
- Track release history and rollback strategy (for example, via preview channels + staged rollout process).

## 5) Practical “go-live” order

1. Validate local + preview deployment.
2. Confirm hosting config and headers.
3. Configure custom domain + TLS status.
4. Set budgets/alerts and verify dashboards.
5. Run production deploy and post-deploy smoke tests.

---

## Suggested follow-up questions

1. What are the highest-priority items in the launch checklist for my specific stack (SPA, SSR, or static)?
2. What is the recommended `firebase.json` setup for my routing, caching, and security headers?
3. How should I structure cost alerts and usage thresholds for an expected traffic profile?
