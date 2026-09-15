#!/usr/bin/env bash
# Verification: render, then run every scripted check in order.
# Exits non-zero if any check fails. Does NOT perform the human-browser
# checks (opening the site/deck, exercising the interactive and its
# fallback, opening the deck with the network disabled) -- those are
# documented separately in docs/build-log.md and require a real browser,
# which this environment does not have installed by design (see
# implementation-plan decision D5).
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

FAIL=0

echo "== 1/7: quarto render =="
if quarto render; then
    echo "PASS: quarto render"
else
    echo "FAIL: quarto render"
    FAIL=1
fi
echo

echo "== 2/7: internal links =="
if python3 scripts/check_links.py; then
    :
else
    FAIL=1
fi
echo

echo "== 3/7: source-claim reconciliation =="
if python3 scripts/check_sources.py; then
    :
else
    FAIL=1
fi
echo

echo "== 4/7: softmax numerical reference =="
if python3 scripts/check_softmax_reference.py; then
    :
else
    FAIL=1
fi
echo

echo "== 5/7: neuron/backprop numerical example =="
if python3 scripts/check_neuron_example.py; then
    :
else
    FAIL=1
fi
echo

echo "== 6/7: transformer path-length numerical example =="
if python3 scripts/check_transformer_path_lengths.py; then
    :
else
    FAIL=1
fi
echo

echo "== 7/7: offline presentation check (static) =="
if python3 scripts/check_offline.py; then
    :
else
    FAIL=1
fi
echo

if [ "$FAIL" -eq 0 ]; then
    echo "ALL SCRIPTED CHECKS PASSED."
    echo "Human-browser checks (interactive, fallback, no-network deck open) are still required -- see docs/build-log.md."
else
    echo "ONE OR MORE SCRIPTED CHECKS FAILED. See output above."
fi

exit "$FAIL"
