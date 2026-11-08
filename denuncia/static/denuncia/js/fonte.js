(function () {
    var PADRAO = 112.5;
    var MINIMO = 87.5;
    var MAXIMO = 150;
    var PASSO = 12.5;
    var CHAVE = 'vigia-fonte';

    var atual = PADRAO;

    try {
        var salvo = parseFloat(localStorage.getItem(CHAVE));
        if (salvo >= MINIMO && salvo <= MAXIMO) atual = salvo;
    } catch (e) {}

    function aplicar(valor) {
        atual = Math.min(MAXIMO, Math.max(MINIMO, valor));
        document.documentElement.style.fontSize = atual + '%';
        try { localStorage.setItem(CHAVE, atual); } catch (e) {}
    }

    aplicar(atual);

    document.getElementById('fonte-aumentar').addEventListener('click', function () {
        aplicar(atual + PASSO);
    });
    document.getElementById('fonte-diminuir').addEventListener('click', function () {
        aplicar(atual - PASSO);
    });
    document.getElementById('fonte-padrao').addEventListener('click', function () {
        aplicar(PADRAO);
    });
})();