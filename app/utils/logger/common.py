from fastapi import Depends, HTTPException, Query


def verify_acc_id(AccId: str = Query(...)):
    if not AccId:
        raise HTTPException(status_code=400, detail="AccId is required")
    return AccId
