let searchParams = new URLSearchParams(window.location.search);

searchParams.has('produtos')
  ? $('#produtos').val(searchParams.get('produtos'))
  : $('#produtos').val(0000);

searchParams.has('tipo_frete')
  ? $('#tipo_frete').val(searchParams.get('tipo_frete'))
  : $('#tipo_frete').val(1);

searchParams.has('preco_frete')
  ? $('#preco_frete').val(searchParams.get('preco_frete'))
  : $('#preco_frete').val(0);

searchParams.has('forma_pgto')
  ? $('#forma_pgto').val(searchParams.get('forma_pgto'))
  : $('#forma_pgto').val('pix');

$('#cep').blur(function () {
  var cep = this.value.replace(/[^0-9]/, '');
  var url = 'https://viacep.com.br/ws/' + cep + '/json/';

  if (cep.length != 8) {
    alert('Cep deve conter 8 dígitos. Ex: 09172180');
    return false;
  }

  $.getJSON(url, function (dadosRetorno) {
    try {
      $('#address_1').val(dadosRetorno.logradouro);
      $('#bairro').val(dadosRetorno.bairro);
      $('#cidade').val(dadosRetorno.localidade);
      $('#estado').val(dadosRetorno.uf);
    } catch (ex) {}
  });
});
