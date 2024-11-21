
function prettify(object) {
  var reader = new commonmark.Parser();
  var writer = new commonmark.HtmlRenderer();
  var parsed = reader.parse(object.innerHTML);
  object.innerHTML = writer.render(parsed);
}
