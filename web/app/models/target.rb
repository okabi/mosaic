class Target < ApplicationRecord
  mount_uploader :path, TargetUploader
end
