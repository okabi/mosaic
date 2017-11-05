module ApplicationHelper
  # form_for の入力フィールド(file_field)となる HTML を返します。
  def form_file_field(form, attribute, label, size: 8, description: nil, example: nil, required: true)
    form_xxxx 'file_field', form, attribute, label, size: size, description: description, example: example, required: required
  end

  # form_for の入力フィールド(number_field)となる HTML を返します。
  def form_number_field(form, attribute, label, size: 8, description: nil, example: nil, required: true)
    form_xxxx 'number_field', form, attribute, label, size: size, description: description, example: example, required: required
  end

  # form_for の submit ボタンとなる HTML を返します。
  def form_submit(form, label, size: 8, type: 'btn-primary')
    "<div class='col-sm-offset-2 col-sm-#{size}'>".html_safe +
      (form.submit label, class: "form-control btn #{type}") +
    "</div>".html_safe
  end

  # Bootstrap の Panel となる HTML を返します。
  def panel(type: 'primary', header: nil, body: nil, footer: nil)
    "<div class='panel panel-#{type}'>".html_safe +
      (header ?
        "<div class='panel-heading'>#{header}</div>" : "").html_safe +
      (body ?
          "<div class='panel-body'>#{body}</div>" : "").html_safe +
      (footer ?
          "<div class='panel-footer'>#{footer}</div>" : "").html_safe +
    "</div>".html_safe
  end

  private

    # form_xxxx (form_text_field や form_text_area) で呼び出されるメソッドです。
    def form_xxxx(xxxx, form, attribute, label, size: 8, description: nil, example: nil, required: true)
      class_options = []
      class_options.push('validation') if required
      class_options.push('form-control') if xxxx != 'file_field'
      html_option = { class: class_options.join(' ') }
      if xxxx == 'number_field'
        html_option[:min] = 0
      elsif xxxx == 'file_field'
        html_option[:accept] = 'image/png,image/gif,image/jpeg'
      end
      "<div class='form-group'>".html_safe +
        form.label(attribute, label, class: 'col-sm-2 control-label') +
        "<div class='col-sm-#{size}'>".html_safe +
        form.send(xxxx, attribute, html_option) +
        (description ?
          "<span class='help-block'>#{description}</span>" : "").html_safe +
        (example ?
          "<span class='help-block'><span class='label label-default'>例</span>#{example}</span>" : "").html_safe +
        "</div>".html_safe +
      "</div>".html_safe
    end
end
