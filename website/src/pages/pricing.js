import React, {useState} from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './pricing.module.css';

const plans = [
  {
    name: 'Explorer',
    description: 'A place to start. Room to experiment.',
    price: 'Free',
    features: [
      '10 public apps',
      '500 credits a month for the agent and builds',
      'Build for Android, iOS (your own devices), web, Windows, macOS and Linux',
      'Shareable download pages, kept 7 days',
      '1 build at a time',
      'Pro agent',
      'Buy more credits any time ($20 for 10,000)',
      '20 MB storage',
      'Community support',
    ],
    action: 'Start building',
    href: 'https://studio.flet.dev',
  },
  {
    name: 'Creator',
    description: 'More space for your next big idea.',
    billing: {
      annual: {price: '$25', note: 'USD · $300 billed annually'},
      monthly: {price: '$30', note: 'USD · billed monthly'},
    },
    trial: '7-day free trial',
    featuresHeading: 'Everything in Explorer, plus:',
    features: [
      '10,000 credits a month',
      'Unlimited public and private apps',
      'Publish to Google Play, the App Store and Microsoft Store',
      'Code signing and notarization for Windows and macOS',
      'GitHub sync',
      'Expert agent',
      '2 builds at a time',
      'Download pages kept 1 year, with named links',
      '100 MB storage',
      'Flet support',
    ],
    action: 'Start building',
    href: 'https://studio.flet.dev',
    featured: true,
  },
  {
    name: 'Studio',
    description: 'A shared space for your whole team.',
    price: 'Coming soon',
    features: ['Multiple users', 'Team collaboration'],
    upcoming: true,
  },
];

// Illustrative workloads, not measured prompt benchmarks. Calculated from
// flet-app/server/app/config.py defaults (September 2026), including Pro's
// 2x markup: Pro 0.0002/input + 0.001/output; Expert 0.002/input + 0.01/output.
// Assumes uncached input and standard context; deployed rates may differ.
const creditExamples = [
  {prompt: 'Change the button color and update the heading.', input: '5,000', output: '1,000', pro: 2, expert: 20},
  {prompt: 'Add a contact form with input validation.', input: '20,000', output: '4,000', pro: 8, expert: 80},
  {prompt: 'Build a task tracker with filters and local storage.', input: '100,000', output: '15,000', pro: 35, expert: 350},
];

function PlanCard({plan, billingPeriod}) {
  const billing = plan.billing?.[billingPeriod];
  return (
    <article className={`${styles.card} ${plan.featured ? styles.featured : ''}`} aria-labelledby={`plan-${plan.name.toLowerCase()}`}>
      <div className={styles.cardHeader}>
        <h2 id={`plan-${plan.name.toLowerCase()}`}>{plan.name}{plan.trial && <span className={`${styles.badge} ${styles.trialBadge}`}>{plan.trial}</span>}</h2>
        <p className={styles.planDescription}>{plan.description}</p>
        <div aria-live={plan.billing ? 'polite' : undefined} aria-atomic="true">
          <p className={`${styles.price} ${plan.upcoming ? styles.upcomingPrice : ''}`}>
            {billing?.price ?? plan.price}{billing && <span> / month</span>}
          </p>
          <p className={styles.priceNote}>{billing?.note ?? (plan.upcoming ? 'Pricing and full details to be announced.' : 'Build at your own pace.')}</p>
        </div>
      </div>
      {plan.featuresHeading && <p className={styles.featuresHeading}>{plan.featuresHeading}</p>}
      <ul className={styles.features}>
        {plan.features.map((feature) => <li key={feature}>{feature}</li>)}
      </ul>
      {plan.upcoming ? (
        <p className={styles.teaser}>Built for creating together. Stay tuned.</p>
      ) : (
        <Link className={`${styles.cta} ${plan.featured ? styles.primaryCta : ''}`} to={plan.href}>
          {plan.action}<span aria-hidden="true">↗</span>
        </Link>
      )}
    </article>
  );
}

export default function Pricing() {
  const [billingPeriod, setBillingPeriod] = useState('annual');

  return (
    <Layout title="Pricing" description="Explore Flet Studio plans: start free with Explorer, build and publish your apps with Creator, and discover the upcoming Studio plan for teams. The Flet framework is free, forever.">
      <main className={styles.page}>
        <header className={styles.hero}>
          <span className={styles.eyebrow}>Pricing</span>
          <h1>Start with an idea.<br /><span>Choose room to grow.</span></h1>
          <p>The Flet framework is free, forever. Choose a Flet Studio plan for building in your browser, with AI by your side.</p>
        </header>

        <div className={styles.billingControls}>
          <div className={styles.billingToggle} role="group" aria-label="Billing period">
            <button type="button" aria-pressed={billingPeriod === 'monthly'} onClick={() => setBillingPeriod('monthly')}>
              Monthly
            </button>
            <button type="button" aria-pressed={billingPeriod === 'annual'} onClick={() => setBillingPeriod('annual')}>
              Annually <span className={styles.badge}>2 months free</span>
            </button>
          </div>
        </div>

        <section className={styles.plans} aria-label="Flet Studio plans">
          {plans.map((plan) => <PlanCard key={plan.name} plan={plan} billingPeriod={billingPeriod} />)}
        </section>

        <aside className={styles.frameworkNote}>
          <strong>Free framework. For every idea.</strong>
          <p>Build and run Flet apps on your own machine, for personal or commercial use. A paid Studio plan is optional.</p>
          <Link to="/docs">Get started with Flet <span aria-hidden="true">→</span></Link>
        </aside>

        <section className={styles.faq} aria-labelledby="faq-title">
          <span className={styles.eyebrow}>A few more details</span>
          <h2 id="faq-title">Frequently asked questions</h2>
          <details className={styles.question} open>
            <summary>Is the Flet framework free?</summary>
            <div className={styles.answer}>
              <p>Yes. The Flet framework is free and open source, and it will always remain so. You can use it to build personal and commercial apps without a paid subscription.</p>
              <p>Flet is the foundation of our own products and services. Its development, quality, and long-term future are our highest priority. Paid Flet Studio plans help us keep investing in that foundation while offering extra convenience and services.</p>
            </div>
          </details>
          <details className={styles.question} open>
            <summary>How do credits work?</summary>
            <div className={styles.answer}>
              <p>Credits pay for the work the AI agent does in Flet Studio and for building your apps. Each agent request uses credits based on the model, the context it reads, and the output it generates. A prompt can involve several steps, so its cost is not fixed by the number of words you type.</p>
              <p>Explorer includes 500 credits per month and the Pro agent. Creator includes 10,000 credits per month and access to both Pro and Expert. Pro and Expert are AI agent tiers, separate from your subscription plan.</p>
              <div className={styles.tableWrapper} role="region" aria-label="Illustrative AI credit costs" tabIndex={0}>
                <table className={styles.creditTable}>
                  <caption>Illustrative costs in credits — actual usage varies.</caption>
                  <thead><tr><th scope="col">Example prompt</th><th scope="col">Pro</th><th scope="col">Expert</th></tr></thead>
                  <tbody>{creditExamples.map((example) => (
                    <tr key={example.prompt}>
                      <th scope="row">“{example.prompt}”</th><td>~{example.pro}</td><td>~{example.expert}</td>
                    </tr>
                  ))}</tbody>
                </table>
              </div>
              <p className={styles.estimateNote}>These are worked examples, not measured averages or quotes. They assume, respectively, {creditExamples.map((example) => `${example.input} input / ${example.output} output`).join('; ')} tokens across the agent’s work, with no cached input or long-context surcharge, using September 2026 default rates. Tokens are the small pieces of text the AI processes. Larger projects, longer conversations, and extra steps can increase the cost; reused context can reduce it. Check Studio for current rates and your actual usage.</p>
              <p>Monthly plan credits reset each month and do not roll over. Need more? On any plan you can buy more credits in Studio, $20 for 10,000. Purchased credits expire 12 months after purchase.</p>
            </div>
          </details>
          <details className={styles.question} open>
            <summary>How much does a build cost?</summary>
            <div className={styles.answer}>
              <p>Builds are charged by the minute while the build machine works on your app: 10 credits a minute on Linux (Android, web and Linux apps), 20 on Windows and 40 on macOS (iOS and macOS apps). Each build is charged at least 4 minutes. Time spent waiting in the queue or preparing the machine is free.</p>
              <p>Studio shows the rate before you start, and the credits used while the build runs.</p>
            </div>
          </details>
          <details className={styles.question} open>
            <summary>How does the free trial work?</summary>
            <div className={styles.answer}>
              <p>Try Creator free for 7 days, with every Creator feature and 500 bonus credits. A card is required. At the end of the trial your plan starts and the card is charged, unless you cancel before. Cancelling during the trial costs nothing. One trial per account, for accounts that haven't subscribed before.</p>
            </div>
          </details>
          <details className={styles.question} open>
            <summary>What does Flet support include?</summary>
            <div className={styles.answer}>
              <p>Every plan gives you access to Flet’s documentation and community support. Ask questions, share ideas, and get help from other developers through our <Link to="/support">community channels</Link>.</p>
              <p>Creator also includes direct support from the Flet team. Email <a href="mailto:hello@flet.dev">hello@flet.dev</a> for help with Flet and Flet Studio, including account and billing questions.</p>
            </div>
          </details>
        </section>
      </main>
    </Layout>
  );
}
