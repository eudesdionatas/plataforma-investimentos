let quantidadeInput;
let precoInput;
let valorInput;

const tipoAtivoPorClasse = {
    rendaFixa: [
        { value: 'FUNDO', label: 'Fundo' },
        { value: 'TITULO_PUBLICO', label: 'Título Público' },
        { value: 'DEBENTURE', label: 'Debênture' },
        { value: 'CDB', label: 'CDB' },
        { value: 'RDB', label: 'RDB' },
        { value: 'LCI', label: 'LCI' },
        { value: 'LCA', label: 'LCA' },
        { value: 'CRI', label: 'CRI' },
        { value: 'CRA', label: 'CRA' }
    ],
    rendaVariavel: [
        { value: 'ACAO', label: 'Ação' },
        { value: 'FII', label: 'FII' },
        { value: 'ETF', label: 'ETF' },
        { value: 'FUNDO_ACOES', label: 'Fundo de ações' },
        { value: 'FUNDO_MULTIMERCADO', label: 'Fundo Multimercado' }
    ]
};

const ondeInvestirRendaVariavel = new Set(['BOLSA_VALORES', 'FUNDOS_INVESTIMENTO']);
const ondeInvestirRendaFixa = new Set(['TESOURO_DIRETO', 'RENDA_FIXA', 'RENDA_FIXA_EUA']);

// Mapa de moedas para locales
const currencyLocales = {
    'BRL': 'pt-BR', 'USD': 'en-US', 'EUR': 'de-DE', 'GBP': 'en-GB',
    'JPY': 'ja-JP', 'CAD': 'en-CA', 'AUD': 'en-AU', 'CHF': 'de-CH',
    'CNY': 'zh-CN', 'SEK': 'sv-SE', 'ARS': 'es-AR', 'CLP': 'es-CL',
    'MXN': 'es-MX', 'PEN': 'es-PE', 'COP': 'es-CO', 'UYU': 'es-UY',
    'PYG': 'es-PY', 'BOB': 'es-BO', 'VEF': 'es-VE', 'KRW': 'ko-KR',
    'INR': 'en-IN', 'RUB': 'ru-RU', 'ZAR': 'en-ZA', 'TRY': 'tr-TR',
    'SGD': 'en-SG', 'HKD': 'zh-HK', 'NZD': 'en-NZ', 'NOK': 'no-NO',
    'DKK': 'da-DK', 'PLN': 'pl-PL', 'CZK': 'cs-CZ', 'HUF': 'hu-HU',
    'ILS': 'he-IL', 'EGP': 'ar-EG'
};

// Formata valor monetário com sempre 2 casas decimais
function formatMoney(value, currency) {
    const locale = currencyLocales[currency] || 'pt-BR';
    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(value);
}

function parseMoneyInput(value) {
    const cleaned = String(value || '').replace(/[^\d.,-]/g, '').trim();
    if (!cleaned) {
        return 0;
    }

    const lastDot = cleaned.lastIndexOf('.');
    const lastComma = cleaned.lastIndexOf(',');
    let normalized = cleaned;

    if (lastDot > lastComma) {
        normalized = cleaned.replace(/,/g, '');
    } else if (lastComma > lastDot) {
        normalized = cleaned.replace(/\./g, '').replace(',', '.');
    } else {
        normalized = cleaned.replace(',', '.');
    }

    const parsed = Number.parseFloat(normalized);
    return Number.isFinite(parsed) ? parsed : 0;
}

function getQuantidade() {
    return parseFloat(quantidadeInput.value) || 0;
}

function setQuantidade(val) {
    if (Math.abs(getQuantidade() - val) < 0.000001) return;
    // Arredonda para 6 casas decimais e remove zeros à direita
    quantidadeInput.value = parseFloat(val.toFixed(6));
}

function adjustQuantidade(delta) {
    const next = Math.max(0, getQuantidade() + delta);
    setQuantidade(next);
    updateCalculations();
}

function getPrecoValue() {
    return (parseInt(precoInput.dataset.digits || '0', 10) || 0) / 100;
}

function setPreco(val) {
    const digits = Math.round(val * 100);
    precoInput.dataset.digits = String(digits);
    renderPreco();
}

function getValorTotalValue() {
    return (parseInt(valorInput.dataset.digits || '0', 10) || 0) / 100;
}

function setValorTotal(val) {
    const digits = Math.round(val * 100);
    valorInput.dataset.digits = String(digits);
    renderValorTotal();
}

function shouldShowMaskedZero(input) {
    return document.activeElement === input;
}

// Atualiza a exibição do campo de preço
function renderPreco() {
    const moeda = document.getElementById('id_moeda').value;
    const preco = getPrecoValue();
    const focused = shouldShowMaskedZero(precoInput);

    if (preco === 0 && !focused) {
        precoInput.value = '';
        return;
    }

    precoInput.value = formatMoney(preco, moeda);
}

// Atualiza a exibição do valor total
function renderValorTotal() {
    const moeda = document.getElementById('id_moeda').value;
    const total = getValorTotalValue();
    const focused = shouldShowMaskedZero(valorInput);

    if (total === 0 && !focused) {
        valorInput.value = '';
        return;
    }

    valorInput.value = formatMoney(total, moeda);
}

// Função central de cálculo baseada no elemento ativo e campos vazios
function updateCalculations() {
    const active = document.activeElement;

    // Só calcula se o usuário estiver interagindo com um dos campos
    if (active !== quantidadeInput && active !== precoInput && active !== valorInput) return;

    const qVal = getQuantidade();
    const pVal = getPrecoValue();
    const vVal = getValorTotalValue();

    const qFilled = qVal > 0.000001;
    const pFilled = pVal > 0.000001;
    const vFilled = vVal > 0.000001;

    if (active === quantidadeInput) {
        if (vFilled && !pFilled) {
            // Cenário 2: Apenas valor total preenchido -> preço = valor / quantidade
            if (qVal !== 0) setPreco(vVal / qVal);
        } else if (pFilled && !vFilled) {
            // Cenário 2: Apenas preço preenchido -> valor total = quantidade * preço
            setValorTotal(qVal * pVal);
        } else if (pFilled && vFilled) {
            // Cenário 3: Preço e valor total preenchidos -> valor total = quantidade * preço
            setValorTotal(qVal * pVal);
        }
    } else if (active === precoInput) {
        if (vFilled && !qFilled) {
            // Cenário 2: Apenas valor total preenchido -> quantidade = valor / preço
            if (pVal !== 0) setQuantidade(vVal / pVal);
        } else if (qFilled && !vFilled) {
            // Cenário 2: Apenas quantidade preenchido -> valor total = quantidade * preço
            setValorTotal(qVal * pVal);
        } else if (qFilled && vFilled) {
            // Cenário 3: Quantidade e valor total preenchidos -> valor total = quantidade * preço
            setValorTotal(qVal * pVal);
        }
    } else if (active === valorInput) {
        if (qFilled && !pFilled) {
            // Cenário 2: Apenas quantidade preenchido -> preço = valor / quantidade
            if (qVal !== 0) setPreco(vVal / qVal);
        } else if (pFilled && !qFilled) {
            // Cenário 2: Apenas preço preenchido -> quantidade = valor / preço
            if (pVal !== 0) setQuantidade(vVal / pVal);
        } else if (qFilled && pFilled) {
            // Cenário 3: Quantidade e preço preenchidos -> quantidade = valor / preço
            if (pVal !== 0) setQuantidade(vVal / pVal);
        }
    }
}

// Configura máscara ATM e listeners
function setupAtmMask(input, renderFunc) {
    input.addEventListener('keydown', function (e) {
        if (e.key >= '0' && e.key <= '9') {
            e.preventDefault();
            let digits = this.dataset.digits || '0';
            if (digits === '0') digits = '';
            digits += e.key;
            if (digits.length > 13) return; // Limite
            this.dataset.digits = digits;
            renderFunc();
            updateCalculations();
        } else if (e.key === 'Backspace') {
            e.preventDefault();
            let digits = this.dataset.digits || '0';
            digits = digits.slice(0, -1) || '0';
            this.dataset.digits = digits;
            renderFunc();
            updateCalculations();
        } else if (!['Tab', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End', 'Delete'].includes(e.key)) {
            e.preventDefault();
        }
    });

    input.addEventListener('focus', function () {
        renderFunc();
    });

    input.addEventListener('blur', function () {
        renderFunc();
        // A independência é garantida pois o updateCalculations só roda com activeElement correto
    });

    // Bloqueia colar/arrastar texto
    input.addEventListener('paste', e => e.preventDefault());
    input.addEventListener('drop', e => e.preventDefault());
    
    // Garante foco no click para mobile/mouse
    input.addEventListener('click', function() { this.focus(); renderFunc(); });
}

function getClassePorOndeInvestir(ondeInvestir) {
    if (ondeInvestirRendaVariavel.has(ondeInvestir)) {
        return 'rendaVariavel';
    }

    if (ondeInvestirRendaFixa.has(ondeInvestir)) {
        return 'rendaFixa';
    }

    return 'todos';
}

function updateNomeAtivoHint(ondeInvestir) {
    const nomeAtivoInput = document.getElementById('id_nome_ativo');
    if (!nomeAtivoInput) return;

    const hintRendaFixa = 'Fundo, Título público, Debênture, CDB, RDB, LCI, LCA, CRI, CRA...';
    const hintRendaVariavel = 'Ticker da Empresa, Fundo Imobiliário, ETF, Fundo de ações, Fundo Multimercado...';
    const classe = getClassePorOndeInvestir(ondeInvestir);
    const hint = classe === 'rendaVariavel' ? hintRendaVariavel : hintRendaFixa;

    // O atributo title exibe o hint nativo ao passar o mouse sobre o campo.
    nomeAtivoInput.title = hint;
}

function updateTipoAtivoOptions(ondeInvestir) {
    const tipoAtivoSelect = document.getElementById('id_tipo');
    if (!tipoAtivoSelect) return;

    const selectedValue = tipoAtivoSelect.value;
    const classe = getClassePorOndeInvestir(ondeInvestir);
    let options = tipoAtivoPorClasse.rendaFixa;

    if (classe === 'rendaVariavel') {
        options = tipoAtivoPorClasse.rendaVariavel;
    } else if (classe === 'todos') {
        options = [...tipoAtivoPorClasse.rendaVariavel, ...tipoAtivoPorClasse.rendaFixa];
    }

    tipoAtivoSelect.innerHTML = '';

    options.forEach(function (optionData) {
        const option = document.createElement('option');
        option.value = optionData.value;
        option.textContent = optionData.label;
        tipoAtivoSelect.appendChild(option);
    });

    const selectedStillExists = options.some(function (optionData) {
        return optionData.value === selectedValue;
    });

    tipoAtivoSelect.value = selectedStillExists ? selectedValue : options[0].value;
}

// Inicialização
function init() {
    quantidadeInput = document.getElementById('id_quantidade');
    precoInput = document.getElementById('id_preco_unitario');
    valorInput = document.getElementById('id_valor_total');

    if (!quantidadeInput || !precoInput || !valorInput) return;

    // Permite que o incremento/decremento seja sempre relativo ao valor atual.
    quantidadeInput.setAttribute('step', 'any');
    quantidadeInput.setAttribute('min', '0');
    quantidadeInput.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowUp') {
            e.preventDefault();
            adjustQuantidade(1);
            return;
        }

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            adjustQuantidade(-1);
            return;
        }

        if (['e', 'E', '+', '-'].includes(e.key)) {
            e.preventDefault();
        }
    });

    // Aplica máscaras e listeners
    setupAtmMask(precoInput, renderPreco);
    setupAtmMask(valorInput, renderValorTotal);

    quantidadeInput.addEventListener('input', updateCalculations);

    // Reformata ao trocar moeda
    document.getElementById('id_moeda').addEventListener('change', function () {
        renderPreco();
        renderValorTotal();
    });

    const ondeInvestirInput = document.getElementById('id_onde_investir');
    if (ondeInvestirInput) {
        ondeInvestirInput.addEventListener('change', function () {
            updateNomeAtivoHint(this.value);
            updateTipoAtivoOptions(this.value);
        });

        updateNomeAtivoHint(ondeInvestirInput.value);
        updateTipoAtivoOptions(ondeInvestirInput.value);
    }

    // Carrega dígitos a partir dos valores iniciais (edit mode ou reload)
    const pVal = parseMoneyInput(precoInput.value);
    precoInput.dataset.digits = String(Math.round(pVal * 100));

    const vVal = parseMoneyInput(valorInput.value);
    valorInput.dataset.digits = String(Math.round(vVal * 100));
    
    renderPreco();
    renderValorTotal();
}

document.addEventListener('DOMContentLoaded', init);
