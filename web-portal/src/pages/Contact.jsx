import { useState } from "react";

export default function Contact() {
  const [sent, setSent] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    setSent(true);
  }

  return (
    <section>
      <h1>Contact</h1>
      {sent ? (
        <p>Thanks! We'll get back to you soon.</p>
      ) : (
        <form onSubmit={handleSubmit} className="form">
          <input type="text" placeholder="Your name" required />
          <input type="email" placeholder="Your email" required />
          <textarea placeholder="Message" rows="4" required />
          <button type="submit">Send</button>
        </form>
      )}
    </section>
  );
}
