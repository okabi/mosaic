# coding: utf-8
require "open3"

class StaticPagesController < ApplicationController
  def home
    @target = Target.new
    @images_num = Image.all.size
    @log = []
    File.open('/home/okabi/Projects/mosaic/web/public/log.txt', 'r') do |file|
      file.each do |s|
        @log.push(s)
      end
    end
  end

  def create
    # バリデーション
    if params['target'] == nil
      flash[:danger] = '画像が選択されていません。'
      redirect_to root_url
      return
    end
    pa = target_params

    # アップロードされた画像を保存してモザイクアート生成開始
    target = Target.new(pa)
    if target.save
      # Python プログラムを実行
      Open3.popen3('python /home/okabi/Projects/mosaic/main.py ' + target.id.to_s + ' > /home/okabi/Projects/mosaic/web/public/log.txt 2>&1')
      flash[:success] = 'モザイクアートを生成しています。しばらくしてからページを更新してください。'
      redirect_to root_url
    else
      flash[:danger] = 'アップロード時にエラーが発生しました。もう一度アップロードしてください。'
      redirect_to root_url
    end
  end

  private

  def target_params
    params.require(:target).permit(:path)
  end
end
