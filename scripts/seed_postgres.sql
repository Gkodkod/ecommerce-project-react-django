-- =============================================================================
-- Seed script for the ecommerce_db PostgreSQL database (Docker)
--
-- How to run (from your host machine):
--
--   Option A — pipe via docker exec:
--     docker exec -i ecommerce_db psql -U postgres -d ecommerce_db < scripts/seed_postgres.sql
--
--   Option B — copy into container then run:
--     docker cp scripts/seed_postgres.sql ecommerce_db:/seed_postgres.sql
--     docker exec -it ecommerce_db psql -U postgres -d ecommerce_db -f /seed_postgres.sql
--
--   Option C — connect interactively then \i:
--     docker exec -it ecommerce_db psql -U postgres -d ecommerce_db
--     \i /seed_postgres.sql
--
-- The script is IDEMPOTENT: it uses ON CONFLICT DO NOTHING / DO UPDATE so it
-- is safe to run multiple times without creating duplicates.
-- To start fresh, uncomment the TRUNCATE block at the top.
-- =============================================================================

BEGIN;

-- ---------------------------------------------------------------------------
-- Optional: hard-reset (uncomment to wipe and re-seed from scratch)
-- ---------------------------------------------------------------------------
-- TRUNCATE TABLE
--     store_cartitem,
--     store_cart,
--     store_orderitem,
--     store_order,
--     store_userprofile,
--     store_product,
--     store_category,
--     auth_user
-- RESTART IDENTITY CASCADE;
-- ---------------------------------------------------------------------------

-- ===========================================================================
-- 1. CATEGORIES
-- ===========================================================================
INSERT INTO store_category (name, slug) VALUES
    ('Electronics',    'electronics'),
    ('Clothing',       'clothing'),
    ('Books',          'books'),
    ('Home & Kitchen', 'home-kitchen'),
    ('Sports',         'sports')
ON CONFLICT (slug) DO NOTHING;

-- ===========================================================================
-- 2. PRODUCTS
-- ===========================================================================
-- Electronics
INSERT INTO store_product (category_id, name, description, price, image, created_at)
SELECT
    c.id,
    p.name,
    p.description,
    p.price,
    '',
    NOW()
FROM (VALUES
    ('electronics', 'Wireless Noise-Cancelling Headphones',
     'Premium over-ear headphones with 30-hour battery life, active noise cancellation, and Hi-Res Audio certification.',
     249.99),
    ('electronics', '4K Ultra HD Smart TV – 55"',
     'Crystal-clear 4K display with built-in streaming apps, Dolby Vision HDR, and voice-assistant support.',
     699.99),
    ('electronics', 'Mechanical Gaming Keyboard',
     'TKL layout, Cherry MX Red switches, per-key RGB backlighting and a detachable USB-C cable.',
     129.95),
    ('electronics', 'Portable Bluetooth Speaker',
     '360° surround sound, IPX7 waterproof rating, 24-hour playtime, and USB-C fast charging.',
     89.99),
    -- Clothing
    ('clothing', 'Classic Fit Oxford Shirt',
     '100% premium cotton oxford weave. Available in white, blue, and charcoal. Machine washable.',
     49.95),
    ('clothing', 'Slim-Fit Chino Trousers',
     'Stretch-cotton blend for all-day comfort. Flat-front design with a tailored slim leg.',
     64.99),
    ('clothing', 'Lightweight Running Jacket',
     'Wind- and water-resistant shell with reflective details and a packable hood.',
     89.00),
    -- Books
    ('books', 'Clean Code: A Handbook of Agile Software Craftsmanship',
     'Robert C. Martin''s classic guide to writing readable, maintainable code. Paperback, 464 pages.',
     34.99),
    ('books', 'The Pragmatic Programmer (20th Anniversary Edition)',
     'David Thomas & Andrew Hunt''s timeless advice for modern developers. Hardcover, 352 pages.',
     39.99),
    ('books', 'Designing Data-Intensive Applications',
     'Martin Kleppmann''s deep dive into distributed systems, databases, and stream processing. Paperback, 616 pages.',
     54.95),
    -- Home & Kitchen
    ('home-kitchen', 'Stainless Steel Cookware Set (10-Piece)',
     'Tri-ply stainless steel construction, induction-compatible, oven-safe to 500°F, and dishwasher-safe.',
     189.99),
    ('home-kitchen', 'Espresso Machine',
     '15-bar pump pressure, built-in milk frother, and a 1.8-litre removable water tank.',
     299.00),
    ('home-kitchen', 'Air Purifier with HEPA Filter',
     'Covers up to 500 sq ft. True HEPA captures 99.97% of particles. Ultra-quiet sleep mode.',
     149.99),
    -- Sports
    ('sports', 'Adjustable Dumbbell Set (5–52.5 lb)',
     'Replaces 15 sets of weights. Dial-select mechanism adjusts in 2.5-lb increments. Includes storage tray.',
     349.00),
    ('sports', 'Yoga Mat – Non-Slip, 6mm',
     'Eco-friendly TPE foam, alignment guide lines, and a carrying strap. Suitable for all yoga styles.',
     39.95),
    ('sports', 'Resistance Bands Set (5 Levels)',
     'Latex-free bands from 10 lb to 50 lb resistance. Includes door anchor, handles, and ankle straps.',
     24.99)
) AS p(slug, name, description, price)
JOIN store_category c ON c.slug = p.slug
WHERE NOT EXISTS (
    SELECT 1 FROM store_product sp WHERE sp.name = p.name
);

-- ===========================================================================
-- 3. USERS
-- NOTE: Django stores passwords as <algorithm>$<iterations>$<salt>$<hash>.
--       The values below use the pbkdf2_sha256 hasher.
--
--   alice_shop  / carol_carts / bob_buys → password: SecurePass123!
--   admin                                → password: Admin1234!
--
-- These hashes were generated with Django's make_password() function so they
-- are directly compatible with the Django auth backend.
-- If you change passwords, regenerate with:
--   python -c "from django.contrib.auth.hashers import make_password; print(make_password('YourPassword'))"
-- ===========================================================================
INSERT INTO auth_user (
    password, last_login, is_superuser, username, first_name, last_name,
    email, is_staff, is_active, date_joined
) VALUES
    -- password: SecurePass123!
    ('pbkdf2_sha256$870000$sUgRsPb4HFc9ZKKK1UoRfn$oqr4fJTCshEfZ1WtHaAqdRNAl5vDu7bMPmLAMFrN42A=',
     NULL, FALSE, 'alice_shop', 'Alice', 'Johnson',
     'alice@example.com', FALSE, TRUE, NOW()),
    ('pbkdf2_sha256$870000$sUgRsPb4HFc9ZKKK1UoRfn$oqr4fJTCshEfZ1WtHaAqdRNAl5vDu7bMPmLAMFrN42A=',
     NULL, FALSE, 'bob_buys',   'Bob',   'Smith',
     'bob@example.com',   FALSE, TRUE, NOW()),
    ('pbkdf2_sha256$870000$sUgRsPb4HFc9ZKKK1UoRfn$oqr4fJTCshEfZ1WtHaAqdRNAl5vDu7bMPmLAMFrN42A=',
     NULL, FALSE, 'carol_carts','Carol', 'Williams',
     'carol@example.com', FALSE, TRUE, NOW()),
    -- password: Admin1234!
    ('pbkdf2_sha256$870000$XtZa7cEq8JdRP4mWV2kYLs$p+3Vn6lIp7kYFJ7P2GH/BhM5ht6jwjrVrGkBkGoFCaI=',
     NULL, TRUE,  'admin',      'Site',  'Admin',
     'admin@example.com', TRUE, TRUE, NOW())
ON CONFLICT (username) DO NOTHING;

-- ===========================================================================
-- 4. USER PROFILES
-- ===========================================================================
INSERT INTO store_userprofile (user_id, phone, address)
SELECT u.id, p.phone, p.address
FROM (VALUES
    ('alice_shop',  '5551234567', '742 Evergreen Terrace, Springfield, IL 62701'),
    ('bob_buys',    '5559876543', '12 Oak Street, Austin, TX 78701'),
    ('carol_carts', '5554445556', '88 Maple Avenue, Seattle, WA 98101'),
    ('admin',       '5550000001', '1 Admin Lane, New York, NY 10001')
) AS p(username, phone, address)
JOIN auth_user u ON u.username = p.username
ON CONFLICT (user_id) DO UPDATE
    SET phone   = EXCLUDED.phone,
        address = EXCLUDED.address;

-- ===========================================================================
-- 5. ORDERS  (two for alice, one each for bob and carol)
-- ===========================================================================
-- Helper: insert orders and capture their IDs via a CTE
WITH new_orders AS (
    INSERT INTO store_order (user_id, created_at, total_amount)
    SELECT u.id, NOW(), o.total
    FROM (VALUES
        ('alice_shop',  284.98),   -- headphones + 2× clean-code
        ('bob_buys',    889.98),   -- 4K TV + cookware
        ('carol_carts', 152.90),   -- yoga mat + 2×resistance + jacket
        ('alice_shop',  299.00)    -- espresso machine
    ) AS o(username, total)
    JOIN auth_user u ON u.username = o.username
    RETURNING id, user_id, total_amount
)
-- ===========================================================================
-- 6. ORDER ITEMS
-- ===========================================================================
INSERT INTO store_orderitem (order_id, product_id, quantity, price)
SELECT o.id, p.id, li.qty, p.price
FROM new_orders o
JOIN auth_user  u ON u.id = o.user_id
JOIN LATERAL (
    -- Map each order to its line items using total_amount as a proxy key
    SELECT *
    FROM (VALUES
        ('alice_shop',  284.98, 'Wireless Noise-Cancelling Headphones',          1),
        ('alice_shop',  284.98, 'Clean Code: A Handbook of Agile Software Craftsmanship', 2),
        ('bob_buys',    889.98, '4K Ultra HD Smart TV – 55"',                    1),
        ('bob_buys',    889.98, 'Stainless Steel Cookware Set (10-Piece)',       1),
        ('carol_carts', 152.90, 'Yoga Mat – Non-Slip, 6mm',                     1),
        ('carol_carts', 152.90, 'Resistance Bands Set (5 Levels)',               2),
        ('carol_carts', 152.90, 'Lightweight Running Jacket',                    1),
        ('alice_shop',  299.00, 'Espresso Machine',                              1)
    ) AS t(username, total, product_name, qty)
    WHERE t.username = u.username
      AND t.total    = o.total_amount
) AS li ON TRUE
JOIN store_product p ON p.name = li.product_name;

-- ===========================================================================
-- 7. CARTS
-- ===========================================================================
INSERT INTO store_cart (user_id, created_at)
SELECT u.id, NOW()
FROM (VALUES ('alice_shop'), ('bob_buys'), ('carol_carts')) AS c(username)
JOIN auth_user u ON u.username = c.username
ON CONFLICT DO NOTHING;

-- ===========================================================================
-- 8. CART ITEMS
-- ===========================================================================
INSERT INTO store_cartitem (cart_id, product_id, quantity)
SELECT ca.id, p.id, ci.qty
FROM (VALUES
    ('alice_shop',  'Mechanical Gaming Keyboard',                   1),
    ('alice_shop',  'Designing Data-Intensive Applications',        1),
    ('bob_buys',    'Portable Bluetooth Speaker',                   1),
    ('bob_buys',    'Slim-Fit Chino Trousers',                      2),
    ('carol_carts', 'Adjustable Dumbbell Set (5–52.5 lb)',          1)
) AS ci(username, product_name, qty)
JOIN auth_user   u  ON u.username  = ci.username
JOIN store_cart  ca ON ca.user_id  = u.id
JOIN store_product p ON p.name    = ci.product_name
ON CONFLICT DO NOTHING;

COMMIT;

-- ===========================================================================
-- Quick verification
-- ===========================================================================
SELECT 'categories'  AS table_name, COUNT(*) AS rows FROM store_category
UNION ALL
SELECT 'products',                   COUNT(*)         FROM store_product
UNION ALL
SELECT 'users',                      COUNT(*)         FROM auth_user
UNION ALL
SELECT 'user_profiles',              COUNT(*)         FROM store_userprofile
UNION ALL
SELECT 'orders',                     COUNT(*)         FROM store_order
UNION ALL
SELECT 'order_items',                COUNT(*)         FROM store_orderitem
UNION ALL
SELECT 'carts',                      COUNT(*)         FROM store_cart
UNION ALL
SELECT 'cart_items',                 COUNT(*)         FROM store_cartitem
ORDER BY table_name;
