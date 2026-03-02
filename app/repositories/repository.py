from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId
from app.database import get_database
from app.services.auth_service import get_password_hash, verify_password
from app.schemas.schemas import (
    UserCreate,
    ProductCreate,
    ProductUpdate,
    WarehouseLocationCreate,
    WarehouseStructureCreate,
    WarehouseStructureUpdate,
    DashboardStats,
)


def serialize_doc(doc: dict) -> dict:
    if doc is None:
        return None
    doc["id"] = str(doc.pop("_id"))
    return doc


class Repository:
    @staticmethod
    async def create_user(user: UserCreate) -> dict:
        db = get_database()
        hashed_password = get_password_hash(user.password)
        doc = {
            "email": user.email,
            "name": user.name,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow(),
        }
        result = await db.users.insert_one(doc)
        doc["_id"] = result.inserted_id
        return serialize_doc(doc)

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[dict]:
        db = get_database()
        user = await db.users.find_one({"email": email})
        return serialize_doc(user) if user else None

    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[dict]:
        user = await Repository.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.get("hashed_password", "")):
            return None
        return user

    @staticmethod
    async def create_product(product: ProductCreate) -> dict:
        db = get_database()
        doc = {
            "sku": product.sku,
            "name": product.name,
            "description": product.description,
            "quantity": product.quantity,
            "category": product.category,
            "location_id": None,
            "created_at": datetime.utcnow(),
        }
        result = await db.products.insert_one(doc)
        doc["_id"] = result.inserted_id
        return serialize_doc(doc)

    @staticmethod
    async def get_products() -> List[dict]:
        db = get_database()
        products = await db.products.find().to_list(1000)
        return [serialize_doc(p) for p in products]

    @staticmethod
    async def get_product_by_id(product_id: str) -> Optional[dict]:
        db = get_database()
        product = await db.products.find_one({"_id": ObjectId(product_id)})
        return serialize_doc(product) if product else None

    @staticmethod
    async def get_product_by_sku(sku: str) -> Optional[dict]:
        db = get_database()
        product = await db.products.find_one({"sku": sku})
        return serialize_doc(product) if product else None

    @staticmethod
    async def update_product(product_id: str, product: ProductUpdate) -> Optional[dict]:
        db = get_database()
        update_data = {k: v for k, v in product.model_dump().items() if v is not None}
        if not update_data:
            return await Repository.get_product_by_id(product_id)

        result = await db.products.find_one_and_update(
            {"_id": ObjectId(product_id)}, {"$set": update_data}, return_document=True
        )
        return serialize_doc(result) if result else None

    @staticmethod
    async def delete_product(product_id: str) -> bool:
        db = get_database()
        result = await db.products.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0

    @staticmethod
    async def search_products(query: str) -> List[dict]:
        db = get_database()
        products = await db.products.find(
            {
                "$or": [
                    {"name": {"$regex": query, "$options": "i"}},
                    {"sku": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}},
                ]
            }
        ).to_list(1000)
        return [serialize_doc(p) for p in products]

    @staticmethod
    async def create_location(location: WarehouseLocationCreate) -> dict:
        db = get_database()
        doc = {
            "percha": location.percha,
            "piso": location.piso,
            "columna": location.columna,
            "is_occupied": False,
            "product_id": None,
            "created_at": datetime.utcnow(),
        }
        result = await db.warehouse_locations.insert_one(doc)
        doc["_id"] = result.inserted_id
        return serialize_doc(doc)

    @staticmethod
    async def get_locations() -> List[dict]:
        db = get_database()
        locations = await db.warehouse_locations.find().to_list(1000)
        return [serialize_doc(l) for l in locations]

    @staticmethod
    async def get_location_by_id(location_id: str) -> Optional[dict]:
        db = get_database()
        location = await db.warehouse_locations.find_one({"_id": ObjectId(location_id)})
        return serialize_doc(location) if location else None

    @staticmethod
    async def get_location_by_coordinates(
        percha: int, piso: int, columna: int
    ) -> Optional[dict]:
        db = get_database()
        location = await db.warehouse_locations.find_one(
            {"percha": percha, "piso": piso, "columna": columna}
        )
        return serialize_doc(location) if location else None

    @staticmethod
    async def delete_location(location_id: str) -> bool:
        db = get_database()
        result = await db.warehouse_locations.delete_one({"_id": ObjectId(location_id)})
        return result.deleted_count > 0

    @staticmethod
    async def create_structure(structure: WarehouseStructureCreate) -> dict:
        db = get_database()
        doc = {
            "name": structure.name,
            "total_perchas": structure.total_perchas,
            "total_pisos": structure.total_pisos,
            "total_columnas": structure.total_columnas,
            "created_at": datetime.utcnow(),
        }
        result = await db.warehouse_structure.insert_one(doc)
        doc["_id"] = result.inserted_id
        return serialize_doc(doc)

    @staticmethod
    async def get_structures() -> List[dict]:
        db = get_database()
        structures = await db.warehouse_structure.find().to_list(100)
        return [serialize_doc(s) for s in structures]

    @staticmethod
    async def get_structure_by_id(structure_id: str) -> Optional[dict]:
        db = get_database()
        structure = await db.warehouse_structure.find_one(
            {"_id": ObjectId(structure_id)}
        )
        return serialize_doc(structure) if structure else None

    @staticmethod
    async def update_structure(
        structure_id: str, structure: WarehouseStructureUpdate
    ) -> Optional[dict]:
        db = get_database()
        update_data = {k: v for k, v in structure.model_dump().items() if v is not None}
        if not update_data:
            return await Repository.get_structure_by_id(structure_id)

        result = await db.warehouse_structure.find_one_and_update(
            {"_id": ObjectId(structure_id)}, {"$set": update_data}, return_document=True
        )
        return serialize_doc(result) if result else None

    @staticmethod
    async def delete_structure(structure_id: str) -> bool:
        db = get_database()
        result = await db.warehouse_structure.delete_one(
            {"_id": ObjectId(structure_id)}
        )
        return result.deleted_count > 0

    @staticmethod
    async def assign_product_to_location(product_id: str, location_id: str) -> bool:
        db = get_database()

        location = await db.warehouse_locations.find_one({"_id": ObjectId(location_id)})
        if not location or location.get("is_occupied"):
            return False

        await db.warehouse_locations.update_one(
            {"_id": ObjectId(location_id)},
            {"$set": {"is_occupied": True, "product_id": product_id}},
        )

        await db.products.update_one(
            {"_id": ObjectId(product_id)}, {"$set": {"location_id": location_id}}
        )
        return True

    @staticmethod
    async def unassign_product_from_location(product_id: str, location_id: str) -> bool:
        db = get_database()

        await db.warehouse_locations.update_one(
            {"_id": ObjectId(location_id)},
            {"$set": {"is_occupied": False, "product_id": None}},
        )

        await db.products.update_one(
            {"_id": ObjectId(product_id)}, {"$set": {"location_id": None}}
        )
        return True

    @staticmethod
    async def get_dashboard_stats() -> DashboardStats:
        db = get_database()

        total_products = await db.products.count_documents({})
        total_locations = await db.warehouse_locations.count_documents({})
        occupied_locations = await db.warehouse_locations.count_documents(
            {"is_occupied": True}
        )
        available_locations = total_locations - occupied_locations
        low_stock_products = await db.products.count_documents(
            {"quantity": {"$lt": 10}}
        )

        return DashboardStats(
            total_products=total_products,
            total_locations=total_locations,
            occupied_locations=occupied_locations,
            available_locations=available_locations,
            low_stock_products=low_stock_products,
        )


repository = Repository()
