import React, {useEffect, useState} from 'react';
import DefaultNavbarItem from '@theme/NavbarItem/DefaultNavbarItem';

const CACHE_KEY = 'flet-github-stars';
const CACHE_TTL = 15 * 60 * 1000;
let pendingRequest;
let cachedStars;

function readCache() {
  if (cachedStars) return cachedStars;
  try {
    const value = JSON.parse(localStorage.getItem(CACHE_KEY));
    if (Number.isSafeInteger(value?.count) && value.count >= 0 &&
        Number.isFinite(value?.updatedAt)) {
      cachedStars = value;
    }
  } catch {
    // Storage may be disabled. The count can still be fetched normally.
  }
  return cachedStars;
}

function fetchStars() {
  if (!pendingRequest) {
    pendingRequest = (async () => {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 8000);
      try {
        const response = await fetch('https://api.github.com/repos/flet-dev/flet', {
          headers: {Accept: 'application/vnd.github+json'},
          signal: controller.signal,
        });
        if (!response.ok) throw new Error('GitHub stars unavailable');
        const {stargazers_count: count} = await response.json();
        if (!Number.isSafeInteger(count) || count < 0) {
          throw new Error('Invalid GitHub star count');
        }
        cachedStars = {count, updatedAt: Date.now()};
        try {
          localStorage.setItem(CACHE_KEY, JSON.stringify(cachedStars));
        } catch {
          // The in-memory cache also avoids requests during navigation.
        }
        return count;
      } finally {
        clearTimeout(timeout);
        pendingRequest = undefined;
      }
    })();
  }
  return pendingRequest;
}

export default function GitHubStars(props) {
  const [count, setCount] = useState(null);

  useEffect(() => {
    let active = true;
    const cached = readCache();
    if (cached) setCount(cached.count);
    if (!cached || Date.now() - cached.updatedAt >= CACHE_TTL) {
      fetchStars().then(value => {
        if (active) setCount(value);
      }).catch(() => {
        // Keep the cached count, or the plain Star link, on network errors.
      });
    }
    return () => { active = false; };
  }, []);

  const label = count === null ? 'GitHub repository' :
    `GitHub repository: ${count.toLocaleString('en-US')} stars`;

  return <DefaultNavbarItem {...props} aria-label={label} title={label}
    label={<span className="header-github-stars" aria-hidden="true">
      <span>☆</span>
      {count === null ? 'Star' : new Intl.NumberFormat('en-US', {
        notation: 'compact', maximumFractionDigits: 1,
      }).format(count)}
    </span>} />;
}
