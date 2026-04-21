"""
Django management command to populate the database with realistic seed data.

Usage (inside Docker):
    docker exec -it django_backend python manage.py seed_data

Options:
    --flush    Drop all existing store data before seeding (default: False)

This command is idempotent when run without --flush: it skips records that
already exist (matched by slug for categories, username for users, etc.).
"""

from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from store.models import (
    Cart,
    CartItem,
    Category,
    Order,
    OrderItem,
    Product,
    UserProfile,
)

# ── Seed data ─────────────────────────────────────────────────────────────── #

CATEGORIES = [
    {"name": "Electronics",    "slug": "electronics"},
    {"name": "Clothing",       "slug": "clothing"},
    {"name": "Books",          "slug": "books"},
    {"name": "Home & Kitchen", "slug": "home-kitchen"},
    {"name": "Sports",         "slug": "sports"},
]

PRODUCTS = [
    # Electronics
    {
        "category_slug": "electronics",
        "name": "Wireless Noise-Cancelling Headphones",
        "description": (
            "Premium over-ear headphones with 30-hour battery life, "
            "active noise cancellation, and Hi-Res Audio certification."
        ),
        "price": Decimal("249.99"),
    },
    {
        "category_slug": "electronics",
        "name": "4K Ultra HD Smart TV – 55\"",
        "description": (
            "Crystal-clear 4K display with built-in streaming apps, "
            "Dolby Vision HDR, and voice-assistant support."
        ),
        "price": Decimal("699.99"),
    },
    {
        "category_slug": "electronics",
        "name": "Mechanical Gaming Keyboard",
        "description": (
            "TKL layout, Cherry MX Red switches, per-key RGB backlighting "
            "and a detachable USB-C cable."
        ),
        "price": Decimal("129.95"),
    },
    {
        "category_slug": "electronics",
        "name": "Portable Bluetooth Speaker",
        "description": (
            "360° surround sound, IPX7 waterproof rating, 24-hour playtime, "
            "and USB-C fast charging."
        ),
        "price": Decimal("89.99"),
    },
    # Clothing
    {
        "category_slug": "clothing",
        "name": "Classic Fit Oxford Shirt",
        "description": (
            "100% premium cotton oxford weave. Available in white, blue, "
            "and charcoal. Machine washable."
        ),
        "price": Decimal("49.95"),
    },
    {
        "category_slug": "clothing",
        "name": "Slim-Fit Chino Trousers",
        "description": (
            "Stretch-cotton blend for all-day comfort. Flat-front design "
            "with a tailored slim leg."
        ),
        "price": Decimal("64.99"),
    },
    {
        "category_slug": "clothing",
        "name": "Lightweight Running Jacket",
        "description": (
            "Wind- and water-resistant shell with reflective details "
            "and a packable hood."
        ),
        "price": Decimal("89.00"),
    },
    # Books
    {
        "category_slug": "books",
        "name": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "description": (
            "Robert C. Martin's classic guide to writing readable, "
            "maintainable code. Paperback, 464 pages."
        ),
        "price": Decimal("34.99"),
    },
    {
        "category_slug": "books",
        "name": "The Pragmatic Programmer (20th Anniversary Edition)",
        "description": (
            "David Thomas & Andrew Hunt's timeless advice for modern developers. "
            "Hardcover, 352 pages."
        ),
        "price": Decimal("39.99"),
    },
    {
        "category_slug": "books",
        "name": "Designing Data-Intensive Applications",
        "description": (
            "Martin Kleppmann's deep dive into distributed systems, databases, "
            "and stream processing. Paperback, 616 pages."
        ),
        "price": Decimal("54.95"),
    },
    # Home & Kitchen
    {
        "category_slug": "home-kitchen",
        "name": "Stainless Steel Cookware Set (10-Piece)",
        "description": (
            "Tri-ply stainless steel construction, induction-compatible, "
            "oven-safe to 500°F, and dishwasher-safe."
        ),
        "price": Decimal("189.99"),
    },
    {
        "category_slug": "home-kitchen",
        "name": "Espresso Machine",
        "description": (
            "15-bar pump pressure, built-in milk frother, and a 1.8-litre "
            "removable water tank. Makes café-quality espresso at home."
        ),
        "price": Decimal("299.00"),
    },
    {
        "category_slug": "home-kitchen",
        "name": "Air Purifier with HEPA Filter",
        "description": (
            "Covers up to 500 sq ft. True HEPA captures 99.97 % of "
            "particles. Ultra-quiet sleep mode."
        ),
        "price": Decimal("149.99"),
    },
    # Sports
    {
        "category_slug": "sports",
        "name": "Adjustable Dumbbell Set (5–52.5 lb)",
        "description": (
            "Replaces 15 sets of weights. Dial-select mechanism adjusts "
            "in 2.5-lb increments. Includes storage tray."
        ),
        "price": Decimal("349.00"),
    },
    {
        "category_slug": "sports",
        "name": "Yoga Mat – Non-Slip, 6mm",
        "description": (
            "Eco-friendly TPE foam, alignment guide lines, and a carrying "
            "strap. Suitable for all yoga styles."
        ),
        "price": Decimal("39.95"),
    },
    {
        "category_slug": "sports",
        "name": "Resistance Bands Set (5 Levels)",
        "description": (
            "Latex-free bands from 10 lb to 50 lb resistance. Includes "
            "door anchor, handles, and ankle straps."
        ),
        "price": Decimal("24.99"),
    },
]

USERS = [
    {
        "username": "alice_shop",
        "email": "alice@example.com",
        "password": "SecurePass123!",
        "first_name": "Alice",
        "last_name": "Johnson",
        "phone": "5551234567",
        "address": "742 Evergreen Terrace, Springfield, IL 62701",
        "is_staff": False,
    },
    {
        "username": "bob_buys",
        "email": "bob@example.com",
        "password": "SecurePass123!",
        "first_name": "Bob",
        "last_name": "Smith",
        "phone": "5559876543",
        "address": "12 Oak Street, Austin, TX 78701",
        "is_staff": False,
    },
    {
        "username": "carol_carts",
        "email": "carol@example.com",
        "password": "SecurePass123!",
        "first_name": "Carol",
        "last_name": "Williams",
        "phone": "5554445556",
        "address": "88 Maple Avenue, Seattle, WA 98101",
        "is_staff": False,
    },
    {
        "username": "admin",
        "email": "admin@example.com",
        "password": "Admin1234!",
        "first_name": "Site",
        "last_name": "Admin",
        "phone": "5550000001",
        "address": "1 Admin Lane, New York, NY 10001",
        "is_staff": True,
        "is_superuser": True,
    },
]

# Orders: list of (username, [(product_name, qty), ...])
ORDERS = [
    (
        "alice_shop",
        [
            ("Wireless Noise-Cancelling Headphones", 1),
            ("Clean Code: A Handbook of Agile Software Craftsmanship", 2),
        ],
    ),
    (
        "bob_buys",
        [
            ("4K Ultra HD Smart TV – 55\"", 1),
            ("Stainless Steel Cookware Set (10-Piece)", 1),
        ],
    ),
    (
        "carol_carts",
        [
            ("Yoga Mat – Non-Slip, 6mm", 1),
            ("Resistance Bands Set (5 Levels)", 2),
            ("Lightweight Running Jacket", 1),
        ],
    ),
    (
        "alice_shop",
        [
            ("Espresso Machine", 1),
        ],
    ),
]

# Cart items: list of (username, [(product_name, qty), ...])
CART_ITEMS = [
    (
        "alice_shop",
        [
            ("Mechanical Gaming Keyboard", 1),
            ("Designing Data-Intensive Applications", 1),
        ],
    ),
    (
        "bob_buys",
        [
            ("Portable Bluetooth Speaker", 1),
            ("Slim-Fit Chino Trousers", 2),
        ],
    ),
    (
        "carol_carts",
        [
            ("Adjustable Dumbbell Set (5–52.5 lb)", 1),
        ],
    ),
]


# ── Command ───────────────────────────────────────────────────────────────── #

class Command(BaseCommand):
    help = "Seed the database with demo ecommerce data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all existing store data before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write(self.style.WARNING("⚠  Flushing existing store data…"))
            CartItem.objects.all().delete()
            Cart.objects.all().delete()
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            UserProfile.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_superuser=False).exclude(pk=1).delete()
            self.stdout.write(self.style.WARNING("   Done.\n"))

        # ── Categories ────────────────────────────────────────────────────── #
        self.stdout.write("📦 Creating categories…")
        category_map: dict[str, Category] = {}
        for data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=data["slug"], defaults={"name": data["name"]}
            )
            category_map[data["slug"]] = cat
            status = "created" if created else "already exists"
            self.stdout.write(f"   [{status}] {cat.name}")

        # ── Products ──────────────────────────────────────────────────────── #
        self.stdout.write("\n🛒 Creating products…")
        product_map: dict[str, Product] = {}
        for data in PRODUCTS:
            cat = category_map[data["category_slug"]]
            prod, created = Product.objects.get_or_create(
                name=data["name"],
                defaults={
                    "category": cat,
                    "description": data["description"],
                    "price": data["price"],
                },
            )
            product_map[data["name"]] = prod
            status = "created" if created else "already exists"
            self.stdout.write(f"   [{status}] {prod.name}  (${prod.price})")

        # ── Users & Profiles ──────────────────────────────────────────────── #
        self.stdout.write("\n👤 Creating users…")
        user_map: dict[str, User] = {}
        for data in USERS:
            is_super = data.get("is_superuser", False)
            is_staff = data.get("is_staff", False)

            if User.objects.filter(username=data["username"]).exists():
                user = User.objects.get(username=data["username"])
                self.stdout.write(f"   [already exists] {user.username}")
            else:
                if is_super:
                    user = User.objects.create_superuser(
                        username=data["username"],
                        email=data["email"],
                        password=data["password"],
                        first_name=data["first_name"],
                        last_name=data["last_name"],
                    )
                else:
                    user = User.objects.create_user(
                        username=data["username"],
                        email=data["email"],
                        password=data["password"],
                        first_name=data["first_name"],
                        last_name=data["last_name"],
                        is_staff=is_staff,
                    )
                self.stdout.write(
                    f"   [created] {user.username}"
                    + (" (superuser)" if is_super else "")
                )

            UserProfile.objects.get_or_create(
                user=user,
                defaults={"phone": data["phone"], "address": data["address"]},
            )
            user_map[data["username"]] = user

        # ── Orders ────────────────────────────────────────────────────────── #
        self.stdout.write("\n📋 Creating orders…")
        for username, items in ORDERS:
            user = user_map[username]
            total = sum(
                product_map[pname].price * qty for pname, qty in items
            )
            
            # Simple idempotency check: does an order with this user/total exist?
            # Not perfect, but prevents massive duplication on container restarts.
            if Order.objects.filter(user=user, total_amount=total).exists():
                order = Order.objects.filter(user=user, total_amount=total).first()
                self.stdout.write(
                    f"   [already exists] Order #{order.id} for {username}"
                )
                continue

            order = Order.objects.create(user=user, total_amount=total)
            for pname, qty in items:
                product = product_map[pname]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=product.price,
                )
            self.stdout.write(
                f"   [created] Order #{order.id} for {username}  (${total:.2f})"
            )

        # ── Carts ─────────────────────────────────────────────────────────── #
        self.stdout.write("\n🛍  Creating carts…")
        for username, items in CART_ITEMS:
            user = user_map[username]
            
            # Use get_or_create now that it's a OneToOneField
            cart, created = Cart.objects.get_or_create(user=user)
            if created:
                self.stdout.write(f"   [created] Cart for {username}")
            else:
                self.stdout.write(f"   [already exists] Cart for {username}")

            for pname, qty in items:
                product = product_map[pname]
                
                # Robust logic for multiple cart items
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart, product=product, defaults={"quantity": qty}
                )
                if not created:
                    cart_item.quantity = qty
                    cart_item.save()
            self.stdout.write(f"   Cart for {username}  ({len(items)} item(s))")

        # ── Summary ───────────────────────────────────────────────────────── #
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Seed complete!\n"
                f"   Categories : {Category.objects.count()}\n"
                f"   Products   : {Product.objects.count()}\n"
                f"   Users      : {User.objects.count()}\n"
                f"   Orders     : {Order.objects.count()}\n"
                f"   Order items: {OrderItem.objects.count()}\n"
                f"   Carts      : {Cart.objects.count()}\n"
                f"   Cart items : {CartItem.objects.count()}\n"
            )
        )
