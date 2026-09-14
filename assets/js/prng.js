/*
 * A seeded pseudo-random number generator (mulberry32).
 *
 * Used only so the softmax-and-sampling interactive is reproducible: the
 * seed is visible and editable on the page, so a presenter's live demo
 * cannot be ambushed by an unlucky draw, and a reader can reproduce a
 * specific sequence exactly.
 *
 * This is NOT cryptographically secure and must never be used for anything
 * other than this teaching demo.
 */
function mulberry32(seed) {
  let a = seed >>> 0;
  return function next() {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
