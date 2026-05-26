import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './styles.module.css';

function Studio() {
  const { siteConfig = {} } = useDocusaurusContext();
  return (
    <Layout title="Flet Studio" description="Flet Studio — placeholder landing page.">
      <main>
        <div className="container margin-bottom--lg">
          <div className={clsx('flet-hero', styles.heroBanner)}>
            <div className="row">
              <div className="col col--12 text--center">
                <h1 className="hero__title">Flet Studio</h1>
                <p className="hero__subtitle">Short tagline goes here.</p>
                <p>Placeholder copy describing what Flet Studio is.</p>
                <div className={styles.buttons}>
                  <Link
                    className={styles.indexCtasGetStartedButton}
                    to="/docs/studio">
                    Read the docs
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

export default Studio;
