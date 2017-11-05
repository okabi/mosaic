class ImagesController < ApplicationController
  def index
    @images = Image.all
  end

  def new
    @image = Image.new
  end

  def create
    pa = image_params

    # バリデーション
    if pa[:path] == nil
      flash[:danger] = '画像が選択されていません。'
      redirect_to new_image_url
      return
    end

    # アップロードされた画像を保存
    image = Image.new(pa)
    if image.save
      # Python プログラムを起動
      system('python assets/main_save.py ' + image.id.to_s)
      flash[:success] = '画像のアップロードが完了しました。'
      redirect_to images_url
    else
      flash[:danger] = 'アップロード時にエラーが発生しました。ファイル名が重複している可能性があります。'
      redirect_to new_image_url
    end
  end

  def edit
  end

  def update
  end

  def destroy
  end

  private

  def image_params
    params.require(:image).permit(:fav_count, :path)
  end
end
