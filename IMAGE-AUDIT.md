# IMAGE AUDIT — El Kot Automotive Palace (generated 2026-09-25)

No `C:\` / `Downloads` / `OneDrive` machine paths found. `localhost` appears only as API base + docs.

## Working / stable (keep — do NOT randomly replace)
- Unsplash vehicle photos (`images.unsplash.com/photo-*?w=800&q=80`): ~20 IDs mapped 1:1 to vehicles in `the car.html`, `backend/prisma/seedNew.js`, `seedUsed.js`, gallery array. Brand mapping preserved (Mercedes->1618843479313, BMW->1555215695, Range Rover->1606664515524, Porsche 911/Cayenne->1503376780353, Lamborghini->1549399542, Ferrari->1592198084033, Rolls->1563720223185, Aston->1583121274602, Audi->1580273916550, etc.).
- Fallback image `photo-1492144534655-ae79c964c9d7` used everywhere via onerror.
- CDN libs: font-awesome cdnjs, Google Fonts Cairo/Amiri.
- Inline SVG noise texture (data URI) for body overlay.

## Unstable (migration path, not deletion)
- Owner avatar: `scontent.faly8-2.fna.fbcdn.net/...697162390...jpg` with expiring `oe=` token → will break. ACTION: admin uploads `assets/owner.jpg` (local) and we swap src; identity preserved (Ahmed El Kot).
- Unsplash hotlinks are TOS-grey for production: keep temporarily (working), migrate per-vehicle to `/uploads/*` or Cloudinary/S3 via new storage abstraction (`backend/src/utils/storage.js`, `POST /api/upload` multi-file). DB `VehicleImage` already supports multi-image + primary + sortOrder.

## Fixed in this update
- Offline `carCard` imgs had NO onerror → added fallback.
- API `apiCard` alt was model-only → now brand+model; added width/height 800x450 (CLS), lazy loading everywhere.
- Gallery images: added onerror fallback + lazy.
- Vehicle page: thumb strip + prev/next + fullscreen + swipe (touch) for multi-image.
- Admin: multi-upload, primary select, delete, alt text — details page auto-uses stored images.