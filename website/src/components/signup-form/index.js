import React, { useEffect, useId, useRef, useState } from "react";
import BrowserOnly from '@docusaurus/BrowserOnly';
import HCaptcha from "@hcaptcha/react-hcaptcha";
import styles from './styles.module.css';

export default function SignupForm() {
    const emailId = useId();
    const [token, setToken] = useState(null);
    const [email, setEmail] = useState("");
    const captchaRef = useRef(null);

    const onSubmit = (event) => {
        event.preventDefault();
        captchaRef.current.execute();
    };

    const onExpire = () => {
        console.log("hCaptcha Token Expired");
    };

    const onError = (err) => {
        console.log(`hCaptcha Error: ${err}`);
    };

    useEffect(() => {
        if (token) {
            const asyncFn = async () => {
                var data = {
                    email: email,
                    captchaToken: token
                };

                // send message
                const response = await fetch("/api/email-signup", {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data),
                });
                const results = await response.json();
                console.log(`Results:`, results);
            };
            asyncFn();
        }
    }, [token, email]);

    return (
        <div id="signup" className={styles.signupForm}>
            <BrowserOnly fallback={<div>Loading...</div>}>
                {() => {
                    if (token) {
                        // signup submitted
                        return <div>Thank you! You will receive the confirmation email shortly.</div>
                    } else if (window.location.href.endsWith('?signup-confirmed')) {
                        // signup confirmed
                        return <div><span style={{ fontSize: '25px', marginRight: '10px' }}>🎉</span>Congratulations! You have successfully subscribed to Flet newsletter.</div>
                    } else {
                        // signup form
                        return <form onSubmit={onSubmit}>
                            <div className={styles.intro}>
                                <span className={styles.eyebrow}>THE FLET NEWSLETTER</span>
                                <h3>A little Flet in your inbox.</h3>
                                <p>Project updates and tutorials, delivered to you.</p>
                            </div>
                            <div className={styles.fields}>
                                <label htmlFor={emailId}>Your email address</label>
                                <div className={styles.inputRow}>
                                <input
                                    id={emailId}
                                    name="email"
                                    autoComplete="email"
                                    required
                                    type="email"
                                    value={email}
                                    placeholder="Your email address"
                                    onChange={(evt) => setEmail(evt.target.value)}
                                />
                                <button type="submit">Subscribe <span aria-hidden="true">↗</span></button>
                                </div>
                                <HCaptcha
                                    sitekey="db49a301-288d-491b-9746-ebd3354dc5ff"
                                    size="invisible"
                                    onVerify={setToken}
                                    onError={onError}
                                    onExpire={onExpire}
                                    ref={captchaRef}
                                />
                            </div>
                        </form>
                    }
                }}
            </BrowserOnly>
        </div>
    );
}
