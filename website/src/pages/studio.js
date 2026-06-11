import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import {useColorMode} from '@docusaurus/theme-common';
import styles from './studio.module.css';

const FEATURES = [
  {
    icon: 'img/pages/studio/file-browser.svg',
    title: 'File Browser',
    description: 'Manage project files directly in the browser.',
  },
  {
    icon: 'img/pages/studio/gallery.svg',
    title: 'Gallery & Templates',
    description: '500+ examples, templates and apps to start from.',
  },
  {
    icon: 'img/pages/studio/fork-edit-share.svg',
    title: 'Fork. Edit. Share.',
    description: 'Collaborate and remix projects effortlessly.',
  },
  {
    icon: 'img/pages/studio/versions.svg',
    title: 'Versions',
    description: 'Restore previous versions anytime.',
  },
  {
    icon: 'img/pages/studio/live-preview.svg',
    title: 'Live Preview',
    description: 'Share apps instantly with a public link.',
  },
  {
    icon: 'img/pages/studio/package-deploy.svg',
    title: 'Package. Deploy.',
    description: 'Cloud builds & publishing.',
    comingSoon: true,
  },
];

function FeatureCard({ icon, title, description, comingSoon }) {
  return (
    <div className={styles.featureCard}>
      <img className={styles.featureIcon} src={useBaseUrl(icon)} alt="" aria-hidden="true" />
      <h3 className={styles.featureTitle}>
        {title}
        {comingSoon && <span className={styles.comingSoonBadge}>Coming soon</span>}
      </h3>
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
      alt="Flet Studio editor with file browser, code area, and live preview panel"
      loading="eager"
      fetchpriority="high"
    />
  );
}

function Studio() {
  return (
    <Layout
      title="Flet Studio — Build cross-platform Python apps in your browser"
      description="A full-featured Python IDE in the browser. No install. No setup.">
      <main>
        <section className={styles.heroBand}>
          <div className={styles.heroInner}>
            <span className={styles.heroSupertitle}>Flet Studio</span>
            <h1 className={styles.heroTitle}>Build cross-platform Python apps in your browser</h1>
            <p className={styles.heroSubtitle}>
              A full-featured Python IDE in the browser. No install. No setup.
            </p>
            <div className={styles.heroCtas}>
              <a
                className={styles.primaryCta}
                href="https://flet.app"
                target="_blank"
                rel="noopener noreferrer">
                Try Flet Studio
              </a>
              <Link className={styles.secondaryCta} to="/docs/studio">
                Read the docs
              </Link>
            </div>
            <HeroScreenshot />
          </div>
        </section>

        <section className={styles.featuresSection}>
          <div className={styles.featuresInner}>
            <h2 className={styles.featuresHeading}>Everything you need to build, in one place</h2>
            <div className={styles.featureGrid}>
              {FEATURES.map((feature) => (
                <FeatureCard key={feature.title} {...feature} />
              ))}
            </div>
          </div>
        </section>

        <section className={styles.closingBand}>
          <div className={styles.closingInner}>
            <h2 className={styles.closingHeading}>Start building with Flet Studio</h2>
            <p className={styles.closingSubtitle}>
              Open the editor in your browser, or dive into the docs.
            </p>
            <div className={styles.closingCtas}>
              <a
                className={styles.primaryCta}
                href="https://flet.app"
                target="_blank"
                rel="noopener noreferrer">
                Try Flet Studio
              </a>
              <Link className={styles.secondaryCta} to="/docs/studio">
                Read the docs
              </Link>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}

export default Studio;
