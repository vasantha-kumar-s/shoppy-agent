import React, { useEffect, useRef, useState } from 'react';

let listener = null;
/** Promise-based replacement for window.confirm. Resolves true/false. */
export function confirmAction(opts) {
  return new Promise(resolve => {
    if (!listener) return resolve(false);
    listener({ title: 'Are you sure?', confirmLabel: 'Confirm', cancelLabel: 'Cancel', danger: false, ...opts, resolve });
  });
}

export function ConfirmHost() {
  const [req, setReq] = useState(null);
  const confirmRef = useRef(null);
  useEffect(() => { listener = setReq; return () => { listener = null; }; }, []);
  useEffect(() => {
    if (!req) return;
    confirmRef.current?.focus();
    const onKey = e => { if (e.key === 'Escape') close(false); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [req]);
  const close = v => { req?.resolve(v); setReq(null); };
  if (!req) return null;
  return (
    <div className="dialog-backdrop" onClick={() => close(false)}>
      <div className="dialog card" role="alertdialog" aria-modal="true" aria-labelledby="confirm-title" onClick={e => e.stopPropagation()}>
        <h3 id="confirm-title">{req.title}</h3>
        {req.description && <p>{req.description}</p>}
        <div className="dialog-actions">
          <button className="btn btn-secondary" onClick={() => close(false)}>{req.cancelLabel}</button>
          <button ref={confirmRef} className={`btn ${req.danger ? 'btn-danger' : 'btn-primary'}`} onClick={() => close(true)}>{req.confirmLabel}</button>
        </div>
      </div>
    </div>
  );
}
