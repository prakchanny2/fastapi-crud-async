
from typing import List

from fastapi import APIRouter, HTTPException, Path

from . import events_crud as crud
from app.api.models import EventDB, EventSchema

router = APIRouter()


@router.post("/", response_model=EventDB, status_code=201)
async def create_event(payload: EventSchema):
    event_id = await crud.post(payload)

    response_object = {
        "id": event_id,
        "title": payload.title,
        "city": payload.city,
        "price_usd": payload.price_usd,
        "seats_left": payload.seats_left,
    }
    return response_object


@router.get("/{id}/", response_model=EventDB)
async def read_event(id: int = Path(..., gt=0)):
    event = await crud.get(id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


@router.get("/", response_model=List[EventDB])
async def read_all_events():
    return await crud.get_all()


@router.put("/{id}/", response_model=EventDB)
async def update_event(
    payload: EventSchema,
    id: int = Path(..., gt=0)
):
    event = await crud.get(id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    event_id = await crud.put(id, payload)

    response_object = {
        "id": event_id,
        "title": payload.title,
        "city": payload.city,
        "price_usd": payload.price_usd,
        "seats_left": payload.seats_left,
    }
    return response_object


@router.delete("/{id}/", response_model=EventDB)
async def delete_event(id: int = Path(..., gt=0)):
    event = await crud.get(id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    await crud.delete(id)

    return event
