/*
 * Softmax and sampling laboratory.
 *
 * Five candidate next tokens for a fixed prompt stem. The user edits the
 * five logits and the temperature; probabilities update live via a
 * numerically stable softmax. "Draw" buttons sample from the resulting
 * categorical distribution using a seeded PRNG (see prng.js), so the
 * empirical frequencies can be compared against the theoretical ones.
 *
 * No dependency, no network call, no build step. Runs entirely client-side.
 * If JavaScript is disabled, the surrounding page shows a static fallback
 * (see _softmax-fallback.qmd) and this file never executes.
 */
(function () {
  "use strict";

  const TOKENS = ["repair", "monitor", "replace", "close", "ignore"];
  const DEFAULT_LOGITS = [2.0, 1.0, 0.5, -0.5, -3.0];
  const DEFAULT_TEMPERATURE = 1.0;
  const DEFAULT_SEED = 42;

  function softmax(logits, temperature) {
    // Numerically stable: subtract the max before exponentiating. This is
    // also the fact the page teaches — softmax is invariant to a constant
    // shift applied to every logit — so it is worth getting right, not
    // just convenient.
    const scaled = logits.map((z) => z / temperature);
    const maxScaled = Math.max(...scaled);
    const exps = scaled.map((s) => Math.exp(s - maxScaled));
    const sumExps = exps.reduce((a, b) => a + b, 0);
    return exps.map((e) => e / sumExps);
  }

  function sampleIndex(probs, rand) {
    const u = rand();
    let cumulative = 0;
    for (let i = 0; i < probs.length; i++) {
      cumulative += probs[i];
      if (u < cumulative) return i;
    }
    return probs.length - 1; // guard against floating-point rounding
  }

  function argmaxIndex(values) {
    let best = 0;
    for (let i = 1; i < values.length; i++) {
      if (values[i] > values[best]) best = i;
    }
    return best;
  }

  function init(root) {
    const logitInputs = Array.from(root.querySelectorAll("[data-logit-slider]"));
    const logitValues = Array.from(root.querySelectorAll("[data-logit-value]"));
    const tempSlider = root.querySelector("[data-temp-slider]");
    const tempValue = root.querySelector("[data-temp-value]");
    const seedInput = root.querySelector("[data-seed]");
    const tableBody = root.querySelector("[data-table-body]");
    const barsContainer = root.querySelector("[data-bars]");
    const readout = root.querySelector("[data-readout]");
    const drawButtons = {
      1: root.querySelector("[data-draw='1']"),
      100: root.querySelector("[data-draw='100']"),
      1000: root.querySelector("[data-draw='1000']"),
    };
    const resetButton = root.querySelector("[data-reset]");

    let logits = DEFAULT_LOGITS.slice();
    let temperature = DEFAULT_TEMPERATURE;
    let seed = DEFAULT_SEED;
    let rand = mulberry32(seed);
    let counts = new Array(TOKENS.length).fill(0);
    let totalDraws = 0;

    function currentProbs() {
      return softmax(logits, temperature);
    }

    function render() {
      const probs = currentProbs();
      const scaled = logits.map((z) => z / temperature);
      const best = argmaxIndex(logits); // argmax on raw logits == argmax on p_i

      // Table.
      tableBody.innerHTML = "";
      TOKENS.forEach((tok, i) => {
        const tr = document.createElement("tr");
        const empiricalP = totalDraws > 0 ? counts[i] / totalDraws : null;
        tr.innerHTML =
          "<td>" +
          tok +
          (i === best ? " <strong>(argmax)</strong>" : "") +
          "</td>" +
          "<td>" +
          logits[i].toFixed(2) +
          "</td>" +
          "<td>" +
          scaled[i].toFixed(2) +
          "</td>" +
          "<td>" +
          Math.exp(scaled[i] - Math.max(...scaled)).toFixed(4) +
          "</td>" +
          "<td>" +
          probs[i].toFixed(4) +
          "</td>" +
          "<td>" +
          (empiricalP === null ? "—" : empiricalP.toFixed(4)) +
          "</td>";
        tableBody.appendChild(tr);
      });

      // Bars: theoretical fill plus an empirical marker line.
      barsContainer.innerHTML = "";
      TOKENS.forEach((tok, i) => {
        const row = document.createElement("div");
        row.className = "bar-row";
        const label = document.createElement("span");
        label.style.width = "5rem";
        label.textContent = tok;
        const track = document.createElement("div");
        track.className = "bar-track";
        const fillTheory = document.createElement("div");
        fillTheory.className = "bar-fill-theory";
        fillTheory.style.width = (probs[i] * 100).toFixed(1) + "%";
        track.appendChild(fillTheory);
        if (totalDraws > 0) {
          const empiricalP = counts[i] / totalDraws;
          const fillEmpirical = document.createElement("div");
          fillEmpirical.className = "bar-fill-empirical";
          fillEmpirical.style.left = (empiricalP * 100).toFixed(1) + "%";
          track.appendChild(fillEmpirical);
        }
        row.appendChild(label);
        row.appendChild(track);
        barsContainer.appendChild(row);
      });

      // Readout: max absolute deviation between empirical and theoretical.
      if (totalDraws > 0) {
        const deviations = probs.map((p, i) => Math.abs(p - counts[i] / totalDraws));
        const maxDev = Math.max(...deviations);
        readout.textContent =
          "Draws: " +
          totalDraws +
          " — max |empirical − theoretical| = " +
          maxDev.toFixed(4);
      } else {
        readout.textContent = "No draws yet.";
      }
    }

    function draw(n) {
      const probs = currentProbs();
      for (let k = 0; k < n; k++) {
        const i = sampleIndex(probs, rand);
        counts[i] += 1;
        totalDraws += 1;
      }
      render();
    }

    function resetDraws() {
      counts = new Array(TOKENS.length).fill(0);
      totalDraws = 0;
      render();
    }

    function resetSeed() {
      seed = parseInt(seedInput.value, 10);
      if (!Number.isFinite(seed)) seed = DEFAULT_SEED;
      rand = mulberry32(seed);
    }

    logitInputs.forEach((slider, i) => {
      slider.addEventListener("input", () => {
        logits[i] = parseFloat(slider.value);
        logitValues[i].textContent = logits[i].toFixed(1);
        render();
      });
    });

    tempSlider.addEventListener("input", () => {
      temperature = parseFloat(tempSlider.value);
      tempValue.textContent = temperature.toFixed(2);
      render();
    });

    seedInput.addEventListener("change", () => {
      resetSeed();
      resetDraws();
    });

    drawButtons[1].addEventListener("click", () => draw(1));
    drawButtons[100].addEventListener("click", () => draw(100));
    drawButtons[1000].addEventListener("click", () => draw(1000));
    resetButton.addEventListener("click", () => {
      logits = DEFAULT_LOGITS.slice();
      temperature = DEFAULT_TEMPERATURE;
      seedInput.value = String(DEFAULT_SEED);
      resetSeed();
      logitInputs.forEach((slider, i) => {
        slider.value = String(logits[i]);
        logitValues[i].textContent = logits[i].toFixed(1);
      });
      tempSlider.value = String(temperature);
      tempValue.textContent = temperature.toFixed(2);
      resetDraws();
    });

    render();
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-softmax-lab]").forEach(init);
  });
})();
