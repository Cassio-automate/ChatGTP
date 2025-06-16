(function() {
  const descInput = document.getElementById('desc');
  const amountInput = document.getElementById('amount');
  const goalInput = document.getElementById('goal');
  const addBtn = document.getElementById('add');
  const itemsList = document.getElementById('items');
  const suggestionDiv = document.getElementById('suggestion');

  const items = [];

  function renderItems() {
    itemsList.innerHTML = '';
    items.forEach(item => {
      const li = document.createElement('li');
      li.textContent = `${item.description}: R$ ${item.amount.toFixed(2)}`;
      itemsList.appendChild(li);
    });
  }

  function calcSuggestion() {
    const total = items.reduce((acc, item) => acc + item.amount, 0);
    const media = total / (items.length || 1);
    let sugestao = '';
    if (goalInput.value && total > parseFloat(goalInput.value)) {
      sugestao = 'Você excedeu sua meta. Considere reduzir gastos.';
    } else {
      const high = items.find(i => i.amount > media * 2);
      if (high) {
        sugestao = `Reduza despesas em '${high.description}'`;
      } else {
        sugestao = 'Seus gastos estão sob controle.';
      }
    }
    suggestionDiv.textContent = sugestao;
  }

  addBtn.addEventListener('click', () => {
    const desc = descInput.value.trim();
    const amt = parseFloat(amountInput.value);
    if (!desc || isNaN(amt)) return;
    items.push({ description: desc, amount: amt });
    descInput.value = '';
    amountInput.value = '';
    renderItems();
    calcSuggestion();
  });
})();
