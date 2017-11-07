class ImagesController < ApplicationController
  def index
    @images = Image.all
    @images.each do |i|
      if i.mean_h.nil?
        i.mean_h = -1
        i.mean_s = -1
        i.mean_v = -1
      end
    end
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
    elsif Image.find_by_path(pa[:path].original_filename) != nil
      flash[:danger] = 'ファイル名が重複しています。'
      redirect_to new_image_url
      return
    end

    # アップロードされた画像を保存
    image = Image.new(pa)
    if image.save
      # Python プログラムを起動
      if Rails.env == 'production'
        system('python /home/okabi/Projects/mosaic/main_save.py ' + image.id.to_s)
      end
      flash[:success] = '画像のアップロードが完了しました。'
      redirect_to images_url
    else
      flash[:danger] = 'アップロード時にエラーが発生しました。もう一度アップロードしてください。'
      redirect_to new_image_url
    end
  end

  def edit
    @image = Image.find_by_id(params[:id])
    if @image.nil?
      redirect_to images_url
      return
    end
  end

  def update
    @image = Image.find_by_id(params[:id])
    pa = params.require(:image).permit(:fav_count)
    if !@image.nil?
      @image.update_attribute('fav_count', pa[:fav_count])
      flash[:success] = '更新が正常に完了しました。'
    end
    redirect_to images_url
  end

  def destroy
    @image = Image.find_by_id(params[:id])
    text = "#{@image.path} を削除しました。"
    if !@image.nil?
      @image.destroy
      flash[:success] = text
    end
    redirect_to images_url
  end

  private

  def image_params
    params.require(:image).permit(:fav_count, :path)
  end
end
