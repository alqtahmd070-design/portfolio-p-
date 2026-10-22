# El Kot Automotive Palace — Full-Stack Dealership Platform

Premium customer site (existing `the car.html` preserved) + Express + Prisma/PostgreSQL backend + Admin dashboard.

## 1) Audit summary (Phase 1)
- Existing project was a single-file site: `the car.html` (~940 lines, inline CSS/JS, RTL Arabic).
- Catalog was hardcoded JS arrays: 16 new/featured + 10 used vehicles, Unsplash remote images, one Facebook owner avatar (unstable).
- No backend, no DB, no vehicle page, no checkout, contact section was display-only.
- Preserved: design tokens (gold #C9A84C / black #080A0E), hero, featured Maybach S680, filters, gallery, owner, WhatsApp 01202022003 / 01021496722, email alqtahmd070@gmail.com.

## 2) Stack
- Frontend: preserved HTML/CSS/JS + new `frontend/` pages (vehicle, checkout, admin) driven by REST API with offline fallback.
- Backend: Node.js + Express, JWT, bcryptjs, helmet, CORS, rate-limit, express-validator, multer, nodemailer.
- DB: PostgreSQL + Prisma (User, Vehicle, VehicleColor, VehicleImage, VehicleFeature, Customer, Order, ContactMessage).

## 3) Run
### Backend
```
cd backend
copy .env.example .env   # set DATABASE_URL + JWT_SECRET
npm install
npx prisma migrate dev --name init
npm run db:seed          # seeds 26 real vehicles + admin admin@elkot-motors.eg / Admin@123456
npm run dev              # :5000
```
Postgres quick start: `createdb elkot_db` (or Docker: `docker run -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres`).

### Frontend
- Open `the car.html` in browser (or `npx serve .`), API base defaults to `http://localhost:5000/api` (override `window.__API_BASE__`).
- Vehicle page: `frontend/vehicle.html?id=<vehicleId>`
- Checkout: `frontend/checkout.html?id=<vehicleId>&color=<color>` (+ order tracking by EK-number)
- Admin: `frontend/admin.html` (login with seeded admin)

## 4) API
- `GET /api/health`
- `POST /api/auth/register | POST /api/auth/login | GET /api/auth/me`
- `GET /api/cars?search=&brand=&category=&condition=&fuelType=&status=&minPrice=&maxPrice=&sort=newest|price_asc|price_desc|discount|oldest&page=&limit=` 
- `GET /api/cars/:id|slug`, `POST/PUT/DELETE /api/cars` (admin), `POST /api/cars/:id/duplicate` (admin)
- `POST /api/orders` (public), `GET /api/orders/:id|orderNumber` (public track), admin `GET /api/orders`, `PUT /api/orders/:id/status`
- `POST /api/contact` (public), admin `GET /api/contact`, `PUT /api/contact/:id`
- `GET /api/admin/dashboard`, `GET /api/admin/customers` (admin)
- `POST /api/upload` (admin, image field `image`, served at `/uploads/*`)

## 5) Payments & email
- `PaymentService` supports VISA/MASTERCARD/MEEZA/VODAFONE_CASH/BANK_TRANSFER/CASH. No card data stored. Without gateway keys every order stays `PENDING` — never faked as paid.
- Nodemailer SMTP via env; if unset, mails are logged as `[MAIL-SKIPPED]` and orders still succeed.

## 6) Images
- All `<img>` use `onerror` fallback to a stable Unsplash image; lazy loading + alt text. Local uploads via `/api/upload`, abstraction ready for S3/Cloudinary (see `STORAGE_PROVIDER`).
- Known risk: owner avatar uses an expiring Facebook CDN URL — replace with a local `assets/owner.jpg` for production.

## 7) Security
- Helmet, CORS allowlist, rate limiting, validation, JWT Bearer, ADMIN guard, bcrypt-12, `.env` excluded via `.gitignore`, consistent `{success,message}` errors without stack leaks in production.

## 8) الصفحات
- `the car.html` = الرئيسية (محفوظة + فورم تواصل فعّال + روابط للكتالوج)
- `frontend/catalog.html` = بحث شامل + فلاتر + ترتيب + صفحات
- `frontend/vehicle.html?id=` = تفاصيل + معرض + ألوان + شراء + واتساب ديناميكي
- `frontend/checkout.html?id=&color=` = شراء + دفع (Pending) + تتبع الطلب
- `frontend/admin.html` = إدارة كاملة (admin@elkot-motors.eg / Admin@123456)

## 9) الشراء من الكارت (§1-16)
- كل كارت (رئيسية/كتالوج/تفاصيل): [واتساب] + [شراء السيارة] — ظاهران دائماً حتى موبايل 320px (flex-column تحت 600px، min-height 48px).
- AVAILABLE → شراء فعّال | RESERVED → محجوزة معطّل | SOLD → تم البيع معطّل (فرونت + باك إند يرفض).
- `checkout.html`: صورة/ماركة/موديل/سنة/حالة/أصلي/خصم/نهائي + اختيار لون إجباري + بيانات + 6 طرق دفع + ملخص + تأكيد طلب الشراء + صفحة نجاح.
- لا توجد رسالة "تم الدفع" مزيفة — كل الطلبات PENDING_PAYMENT. لا تُحفظ أي بيانات بطاقات.
- أرقام الدفع الحساسة ليست في الفرونت — عبر env + `GET /api/payment-info`.

## 10) الصور — التقرير الكامل في IMAGE-AUDIT.md
- لا مسارات Windows. كل الصور البعيدة محفوظة بعلاقتها الصحيحة.
- كل img فيه fallback + lazy + alt. Admin: رفع متعدد + Primary + حذف.
- صورة المالك: assets/owner.jpg أولاً ثم فيسبوك ثم AE.
- التخزين: storage.js (local الآن، Cloudinary/S3 لاحقاً).
