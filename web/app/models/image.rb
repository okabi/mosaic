class Image < ApplicationRecord
  mount_uploader :path, PictureUploader
end
