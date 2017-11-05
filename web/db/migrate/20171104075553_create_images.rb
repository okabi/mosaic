class CreateImages < ActiveRecord::Migration[5.0]
  def change
    create_table :images do |t|
      t.string :path, :null => false, :unique => true
      t.float :mean_h
      t.float :mean_s
      t.float :mean_v
      t.integer :fav_count, :default => 0

      t.timestamps
    end
  end
end
