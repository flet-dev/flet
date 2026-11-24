
import React from 'react';
import styles from './styles.module.css';
import clsx from 'clsx';

export default function Card(props) {

    return props.href ? <a
        href={props.href}
        className={clsx('card padding--md', styles.cardContainer)}>
        {props.children}
    </a> : <div className={clsx('card padding--md', styles.cardContainer)}>
        {props.children}
    </div>
};