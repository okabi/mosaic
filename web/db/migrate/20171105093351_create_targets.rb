class CreateTargets < ActiveRecord::Migration[5.0]
  def change
    create_table :targets do |t|
      t.string :path

      t.timestamps
    end
  end
end
