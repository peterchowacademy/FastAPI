SELECT * FROM products ORDER BY id LIMIT 5 OFFSET 2 --- select the top 5 results but skip the first top 2 items

INSERT INTO products (name, price, inventory) VALUES ('tortilla', 4, 100); --- insert rows and values

INSERT INTO products (price, name, inventory) VALUEs (10000, 'car', 1000) returning * --- return * give you all the new columns

INSERT INTO products (price, name, inventory) VALUES  (50, 'laptop', 28), (60, 'monitor', 4) returning id, name, created_at; -- insert multiple rows and return specific columns

DELETE FROM products WHERE id = 11 RETURNING *; --- delete a row and show all columns of deleted row

DELETE FROM products WHERE inventory = 0;
SELECT * FROM products; --- delete everything of inventory = 0 and show all results

UPDATE products SET name = 'flour tortilla', price = 40 WHERE id = 14; --- update the columns of the product from id

UPDATE products SET is_sale = true WHERE id > 15 RETURNING *; --- update multiple rows