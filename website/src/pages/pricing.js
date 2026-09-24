import React from 'react';
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
      '1 user',
      '20 MB storage',
      '1,000 AI credits / month',
      'Pro AI agent',
      'Community support',
    ],
    action: 'Start building',
    href: 'https://studio.flet.dev',
  },
  {
    name: 'Creator',
    description: 'More space for your next big idea.',
    price: '$30',
    features: [
      'Unlimited public apps',
      'Unlimited private apps',
      '1 user',
      '100 MB storage',
      '10,000 AI credits / month',
      'Pro & Expert AI agents',
      'Flet support',
    ],
    action: 'Start building',
    href: 'https://studio.flet.dev/pricing',
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

function PlanCard({plan}) {
  return (
    <article className={`${styles.card} ${plan.featured ? styles.featured : ''}`} aria-labelledby={`plan-${plan.name.toLowerCase()}`}>
      <div className={styles.cardHeader}>
        <h2 id={`plan-${plan.name.toLowerCase()}`}>{plan.name}</h2>
        <p className={styles.planDescription}>{plan.description}</p>
        <p className={`${styles.price} ${plan.upcoming ? styles.upcomingPrice : ''}`}>
          {plan.price}{plan.featured && <span> / month</span>}
        </p>
        <p className={styles.priceNote}>{plan.upcoming ? 'Pricing and full details to be announced.' : plan.featured ? 'USD · billed monthly' : 'Build at your own pace.'}</p>
      </div>
      <ul className={styles.features}>
        {plan.features.map((feature) => <li key={feature}>{feature}</li>)}
        <li><span>Packaging & publishing <span className={styles.badge}>Coming soon</span></span></li>
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
  return (
    <Layout title="Pricing" description="Explore Flet Studio plans: start free with Explorer, grow with Creator, and discover the upcoming Studio plan for teams. The Flet framework is free, forever.">
      <main className={styles.page}>
        <header className={styles.hero}>
          <span className={styles.eyebrow}>Pricing</span>
          <h1>Start with an idea.<br /><span>Choose room to grow.</span></h1>
          <p>The Flet framework is free, forever. Choose a Flet Studio plan for building in your browser, with AI by your side.</p>
        </header>

        <section className={styles.plans} aria-label="Flet Studio plans">
          {plans.map((plan) => <PlanCard key={plan.name} plan={plan} />)}
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
            <summary>How do AI credits work?</summary>
            <div className={styles.answer}>
              <p>AI credits pay for the work the AI agent does in Flet Studio. Each request uses credits based on the model, the context it reads, and the output it generates. A prompt can involve several steps, so its cost is not fixed by the number of words you type.</p>
              <p>Explorer includes 1,000 credits per month and the Pro agent. Creator includes 10,000 credits per month and access to both Pro and Expert. Pro and Expert are AI agent tiers, separate from your subscription plan.</p>
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
              <p>Monthly plan credits reset each month and do not roll over. Need more? You can buy additional credits in Studio. Purchased credits do not expire while your account remains active.</p>
            </div>
          </details>
          <details className={styles.question} open>
            <summary>What does Flet support include?</summary>
            <div className={styles.answer}>
              <p>Every plan gives you access to Flet’s documentation and community support. Ask questions, share ideas, and get help from other developers through our <Link to="/support">community channels</Link>.</p>
              <p>Creator also includes direct support from the Flet team. Email <a href="mailto:hello@flet.dev">hello@flet.dev</a> for help with Flet and Flet Studio, including account and billing questions. When reporting a problem, include the steps to reproduce it and any relevant error messages so we can help you more effectively.</p>
            </div>
          </details>
        </section>
      </main>
    </Layout>
  );
}
