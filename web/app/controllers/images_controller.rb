# -*- coding: utf-8 -*-
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
    elsif Image.find_by_path(pa[:path].original_filename) != nil
      flash[:danger] = 'ファイル名が重複しています。'
      redirect_to new_image_url
      return
    end

    # アップロードされた画像を保存
    image = Image.new(pa)
    if image.save
      # Python プログラムを起動
      system('python /home/okabi/Projects/mosaic/main_save.py ' + image.id.to_s)
      flash[:success] = '画像のアップロードが完了しました。'
      redirect_to images_url
    else
      flash[:danger] = 'アップロード時にエラーが発生しました。もう一度アップロードしてください。'
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
