import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './styles.module.css';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import SignupForm from '@site/src/components/signup-form'
import CodeBlock from '@theme/CodeBlock';

const features = [
  {
    title: <>Single code base for any device</>,
    imageUrl: 'img/pages/home/single-code-base.svg',
    description: (
      <>
        Your app will look equally great on iOS, Android, Windows, Linux, macOS and web.
      </>
    ),
  },
  {
    title: <>Build an entire app in Python</>,
    imageUrl: 'img/pages/home/python.svg',
    description: (
      <>
        Build a cross-platform app without knowledge of Dart, Swift, Kotlin, HTML or JavaScript - only Python!
      </>
    ),
  },
  {
    title: <>150+ built-in controls and services</>,
    imageUrl: 'img/pages/home/controls.svg',
    description: (
      <>
        Beautiful UI widgets with Material and Cupertino design: layout, navigation, dialogs, charts - Flet uses Flutter to render UI.
      </>
    ),
  },
  {
    title: <>50+ Python packages for iOS and Android</>,
    imageUrl: 'img/pages/home/python-packages.svg',
    description: (
      <>
        Numpy, pandas, pydantic, cryptography, opencv, pillow and other popular libraries.
      </>
    ),
  },
  {
    title: <>Full web support</>,
    imageUrl: 'img/pages/home/web-support.svg',
    description: (
      <>
        Flet apps run natively in modern browsers using WebAssembly and Pyodide, with no server required. Prefer server-side? Deploy as a Python web app with real-time UI updates.
      </>
    ),
  },
  {
    title: <>Built-in packaging</>,
    imageUrl: 'img/pages/home/packaging.svg',
    description: (
      <>
        Build standalone executables or bundles for iOS, Android, Windows, Linux, macOS and web. Instantly deploy to App Store and Google Play.
      </>
    ),
  },
  {
    title: <>Test on iOS and Android</>,
    imageUrl: 'img/pages/home/test-on-ios-android.svg',
    description: (
      <>
        Test your project on your own mobile device with Flet App. See your app updates as you make changes.
      </>
    ),
  },
  {
    title: <>Extensible</>,
    imageUrl: 'img/pages/home/extensible.svg',
    description: (
      <>
        Easily wrap any of thousands of Flutter packages to use with Flet or build new controls in pure Python using built-in UI primitives.
      </>
    ),
  },
  {
    title: <>Accessible</>,
    imageUrl: 'img/pages/home/accessible.svg',
    description: (
      <>
        Flet is built with Flutter which has solid accessibility foundations on Android, iOS, web, and desktop.
      </>
    ),
  },
];

function Feature({ imageUrl, title, description }) {
  const imgUrl = useBaseUrl(imageUrl);
  return (
    <div className={clsx('col col--4', styles.feature)}>
      {imgUrl && (
        <div className="text--center">
          <img className={styles.featureImage} src={imgUrl} alt={title} />
        </div>
      )}
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}

function Home() {
  const context = useDocusaurusContext();
  const { siteConfig = {} } = context;
  return (
    <Layout
      title={`${siteConfig.customFields.heroTitle}`}
      description={`${siteConfig.tagline}`}>
      <main>
        <div className="container margin-bottom--lg">
          <div className={clsx('flet-hero', styles.heroBanner)}>
            <div className="row">
              <div className="col col--6">
                <img src="img/pages/home/flet-home.png" style={{ width: '90%', marginTop: '1.5rem' }}></img>
              </div>
              <div className="col col--6">
                <h1 className="hero__title">{siteConfig.customFields.heroTitle}</h1>
                <p className="hero__subtitle">{siteConfig.customFields.heroSubTitle}</p>
                <div className={styles.buttons}>
                  <Link
                    className={styles.indexCtasGetStartedButton}
                    to={useBaseUrl('https://docs.flet.dev')}>
                    Get Started
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className={clsx('container', 'text--center', styles.featuresSection)}>
          <h2>Flet awesome features</h2>
          {features && features.length > 0 && (
            <section className={styles.features}>
              <div className="container">
                <div className="row">
                  {features.map((props, idx) => (
                    <Feature key={idx} {...props} />
                  ))}
                </div>
              </div>
            </section>
          )}
        </div>
        <SignupForm />
      </main>
    </Layout>
  );
}

export default Home;