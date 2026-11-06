import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import {useColorMode} from '@docusaurus/theme-common';
import styles from './studio.module.css';

const STEPS = [
  {
    title: 'Describe',
    description: 'Tell the AI agent what to build, or write the Python yourself. Start from scratch or from one of 500+ examples.',
  },
  {
    title: 'Preview',
    description: 'Your app runs beside the code and updates as you change it. Try it at phone and desktop sizes.',
  },
  {
    title: 'Publish',
    description: 'Build it in the cloud for every platform, sign it, and send it to the app stores or a download page.',
  },
];

const GROUPS = [
  {
    title: 'Build with an agent, or by hand',
    features: [
      {
        icon: 'img/pages/home/ai-assistance.svg',
        title: 'AI coding agent',
        description: 'Describe your idea, add features, or fix bugs with the Pro and Expert agents. Review each change as it lands.',
      },
      {
        icon: 'img/pages/studio/file-browser.svg',
        title: 'Browser IDE',
        description: 'Write Python, manage project files, and restore earlier versions, all in your browser with no setup.',
      },
      {
        icon: 'img/pages/studio/live-preview.svg',
        title: 'Live preview',
        description: 'Run your app beside the editor and see each change right away. Share it with a public link.',
      },
      {
        icon: 'img/pages/studio/gallery.svg',
        title: 'Gallery and templates',
        description: 'Start from 500+ examples, templates, and apps. Open one in Studio and make it your own.',
      },
    ],
  },
  {
    title: 'Ship it everywhere',
    features: [
      {
        icon: 'img/pages/studio/cloud-builds.svg',
        title: 'Cloud builds',
        description: 'Android, iOS, Windows, macOS, Linux, and web, built in the cloud. Follow each run’s steps and logs as it goes.',
        to: '/docs/studio/publishing',
      },
      {
        icon: 'img/pages/studio/package-deploy.svg',
        title: 'App stores',
        description: 'Publish to Google Play, the App Store, TestFlight, the Mac App Store, and the Microsoft Store. Studio handles the signing keys, certificates, and profiles.',
        to: '/docs/studio/publishing/signing-keys-and-store-accounts',
        badge: 'Creator',
      },
      {
        icon: 'img/pages/studio/download-page.svg',
        title: 'Download pages',
        description: 'Every app gets a public page at get.flet.app with its latest builds and a QR code, so anyone can install it.',
        to: '/docs/studio/publishing/download-page',
      },
      {
        icon: 'img/pages/studio/github-sync.svg',
        title: 'GitHub sync',
        description: 'Connect a repository and changes go both ways: Studio commits your edits, and your pushes show up in Studio.',
        to: '/docs/studio/github',
        badge: 'Creator',
      },
    ],
  },
];

function FeatureCard({ icon, title, description, to, badge }) {
  return (
    <div className={styles.featureCard}>
      <img className={styles.featureIcon} src={useBaseUrl(icon)} alt="" aria-hidden="true" />
      <h4 className={styles.featureTitle}>
        {to ? <Link to={to}>{title}</Link> : title}
        {badge && <span className={styles.planBadge}>{badge}</span>}
      </h4>
      <p className={styles.featureDescription}>{description}</p>
    </div>
  );
}

function HeroScreenshot() {
  const {colorMode} = useColorMode();
  const heroImageLight = useBaseUrl('img/pages/studio/flet-studio-light.png');
  const heroImageDark = useBaseUrl('img/pages/studio/flet-studio-dark.png');
  return (
    <img
      className={styles.heroScreenshot}
      src={colorMode === 'dark' ? heroImageDark : heroImageLight}
      alt="Flet Studio with the AI agent, the code editor, and a live preview of the app"
      loading="eager"
      fetchPriority="high"
    />
  );
}

function PrimaryCta() {
  return (
    <a
      className={styles.primaryCta}
      href="https://studio.flet.dev"
      target="_blank"
      rel="noopener noreferrer">
      Start free <span aria-hidden="true">↗</span>
    </a>
  );
}

function Studio() {
  return (
    <Layout
      title="Flet Studio | Build and publish Python apps in your browser"
      description="Describe your app to an AI agent, try it live, then build it for every platform and publish it to the app stores. Nothing to install.">
      <main>
        <section className={styles.heroBand}>
          <div className={styles.heroInner}>
            <span className={styles.heroSupertitle}>New · Flet Studio 2.0</span>
            <h1 className={styles.heroTitle}>From idea to app store, <span>in your browser.</span></h1>
            <p className={styles.heroSubtitle}>
              Describe your app to the AI agent, try it live, then build it for Android, iOS, Windows,
              macOS, Linux, and web, and publish it to the stores. Nothing to install.
            </p>
            <div className={styles.heroCtas}>
              <PrimaryCta />
              <Link className={styles.secondaryCta} to="/docs/studio">
                Read the docs <span aria-hidden="true">→</span>
              </Link>
            </div>
            <p className={styles.heroNote}>
              Free plan · 7-day Creator trial · <Link to="/pricing">See pricing</Link>
            </p>
            <HeroScreenshot />
          </div>
        </section>

        <section className={styles.stepsSection}>
          <div className={styles.featuresInner}>
            <h2 className={styles.featuresHeading}>How it works</h2>
            <ol className={styles.steps}>
              {STEPS.map((step, i) => (
                <li key={step.title} className={styles.step}>
                  <span className={styles.stepNumber} aria-hidden="true">{i + 1}</span>
                  <h3 className={styles.stepTitle}>{step.title}</h3>
                  <p className={styles.featureDescription}>{step.description}</p>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section className={styles.featuresSection}>
          <div className={styles.featuresInner}>
            <h2 className={styles.featuresHeading}>Everything from the first line to the app store</h2>
            {GROUPS.map((group) => (
              <div key={group.title} className={styles.featureGroup}>
                <h3 className={styles.groupHeading}>{group.title}</h3>
                <div className={styles.featureGrid}>
                  {group.features.map((feature) => (
                    <FeatureCard key={feature.title} {...feature} />
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className={styles.pricingSection}>
          <div className={styles.featuresInner}>
            <div className={styles.pricingBand}>
              <div>
                <h2 className={styles.pricingHeading}>Free to start</h2>
                <p className={styles.pricingText}>
                  Explorer is free, with 500 credits a month for the agent and builds. Creator adds private
                  apps, store publishing, paid code signing, and GitHub sync. Try it free for 7 days.
                </p>
              </div>
              <Link className={styles.secondaryCta} to="/pricing">
                See pricing <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
        </section>

        <section className={styles.closingBand}>
          <div className={styles.closingInner}>
            <h2 className={styles.closingHeading}>Start building with Flet Studio</h2>
            <p className={styles.closingSubtitle}>
              Open Studio in your browser and take your app from an idea to the app stores.
            </p>
            <div className={styles.closingCtas}>
              <PrimaryCta />
              <Link className={styles.secondaryCta} to="/docs/studio">
                Read the docs <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}

export default Studio;
