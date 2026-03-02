from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.repositories.repository import repository
from app.schemas.schemas import (
    ProductCreate,
    ProductUpdate,
    WarehouseLocationCreate,
    WarehouseStructureCreate,
    WarehouseStructureUpdate,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def is_authenticated(request: Request) -> bool:
    return "access_token" in request.cookies


def get_user_name(request: Request) -> str:
    return request.cookies.get("user_name", "Usuario")


@router.get("/", name="index")
async def index(request: Request):
    if is_authenticated(request):
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/dashboard", name="dashboard")
async def dashboard(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")

    stats = await repository.get_dashboard_stats()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "stats": stats, "user_name": get_user_name(request)},
    )


@router.get("/products", name="products")
async def products_page(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")

    products = await repository.get_products()
    locations = await repository.get_locations()
    return templates.TemplateResponse(
        "products.html",
        {
            "request": request,
            "products": products,
            "locations": locations,
            "user_name": get_user_name(request),
        },
    )


@router.post("/products/create")
async def create_product(request: Request, product: ProductCreate):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")

    existing = await repository.get_product_by_sku(product.sku)
    if existing:
        products = await repository.get_products()
        locations = await repository.get_locations()
        return templates.TemplateResponse(
            "products.html",
            {
                "request": request,
                "products": products,
                "locations": locations,
                "error": "El SKU ya existe",
                "user_name": get_user_name(request),
            },
        )

    await repository.create_product(product)
    return RedirectResponse(url="/products", status_code=303)


@router.post("/products/update/{product_id}")
async def update_product(product_id: str, request: Request, product: ProductUpdate):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")

    await repository.update_product(product_id, product)
    return RedirectResponse(url="/products", status_code=303)


@router.post("/products/delete/{product_id}")
async def delete_product(product_id: str, request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")

    await repository.delete_product(product_id)
    return RedirectResponse(url="/products", status_code=303)


@router.post("/products/assign/{product_id}")
async def assign_product_location(product_id: str, request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")

    form = await request.form()
    location_id = form.get("location_id")

    if location_id:
        await repository.assign_product_to_location(product_id, location_id)

    return RedirectResponse(url="/products", status_code=303)


@router.get("/locations", name="locations")
async def locations_page(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")

    locations = await repository.get_locations()
    return templates.TemplateResponse(
        "locations.html",
        {
            "request": request,
            "locations": locations,
            "user_name": get_user_name(request),
        },
    )


@router.post("/locations/create")
async def create_location(request: Request, location: WarehouseLocationCreate):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")

    existing = await repository.get_location_by_coordinates(
        location.percha, location.piso, location.columna
    )
    if existing:
        locations = await repository.get_locations()
        return templates.TemplateResponse(
            "locations.html",
            {
                "request": request,
                "locations": locations,
                "error": "La ubicación ya existe",
                "user_name": get_user_name(request),
            },
        )

    await repository.create_location(location)
    return RedirectResponse(url="/locations", status_code=303)


@router.post("/locations/delete/{location_id}")
async def delete_location(location_id: str, request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")

    await repository.delete_location(location_id)
    return RedirectResponse(url="/locations", status_code=303)


@router.get("/structure", name="structure")
async def structure_page(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")

    structures = await repository.get_structures()
    return templates.TemplateResponse(
        "structure.html",
        {
            "request": request,
            "structures": structures,
            "user_name": get_user_name(request),
        },
    )


@router.post("/structure/create")
async def create_structure(request: Request, structure: WarehouseStructureCreate):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")

    await repository.create_structure(structure)

    total = structure.total_perchas * structure.total_pisos * structure.total_columnas
    for percha in range(1, structure.total_perchas + 1):
        for piso in range(1, structure.total_pisos + 1):
            for columna in range(1, structure.total_columnas + 1):
                await repository.create_location(
                    WarehouseLocationCreate(percha=percha, piso=piso, columna=columna)
                )

    return RedirectResponse(url="/structure", status_code=303)


@router.post("/structure/update/{structure_id}")
async def update_structure(
    structure_id: str, request: Request, structure: WarehouseStructureUpdate
):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")

    await repository.update_structure(structure_id, structure)
    return RedirectResponse(url="/structure", status_code=303)


@router.post("/structure/delete/{structure_id}")
async def delete_structure(structure_id: str, request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")

    await repository.delete_structure(structure_id)
    return RedirectResponse(url="/structure", status_code=303)


@router.get("/search", name="search")
async def search_page(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")

    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "results": [],
            "query": "",
            "user_name": get_user_name(request),
        },
    )


@router.post("/search")
async def search_products(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")

    form = await request.form()
    query = form.get("query", "")

    if not query:
        return templates.TemplateResponse(
            "search.html",
            {
                "request": request,
                "results": [],
                "query": "",
                "user_name": get_user_name(request),
            },
        )

    products = await repository.search_products(query)

    for product in products:
        if product.get("location_id"):
            location = await repository.get_location_by_id(product["location_id"])
            product["location"] = location
        else:
            product["location"] = None

    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "results": products,
            "query": query,
            "user_name": get_user_name(request),
        },
    )
