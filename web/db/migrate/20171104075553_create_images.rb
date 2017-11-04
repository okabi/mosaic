class CreateImages < ActiveRecord::Migration[5.0]
  def change
    create_table :images do |t|
      t.string :path, :null => false, :unique => true
      t.float :mean_h, :null => false
      t.float :mean_s, :null => false
      t.float :mean_v, :null => false
      t.integer :fav_count, :null => false, :default => 0

      t.timestamps
    end
  end
end
