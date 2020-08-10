#!/usr/bin/python3

import pytest
from brownie import Wei, reverts

@pytest.fixture(scope="module", autouse=True)
def loanSettings(LoanSettings, accounts, bzx):
    bzx.replaceContract(accounts[0].deploy(LoanSettings).address)

def test_setup_removeLoanParams(Constants, bzx, accounts, SUSD, WETH):

    loanParams = {
        "id": "0x0",
        "active": False,
        "owner": Constants["ZERO_ADDRESS"],
        "loanToken": SUSD.address,
        "collateralToken": WETH.address,
        "initialMargin": Wei("50 ether"),
        "maintenanceMargin": Wei("15 ether"),
        "fixedLoanTerm": "2419200"
    }
    tx = bzx.setupLoanParams([list(loanParams.values())])

    loanParamsId = tx.events["LoanParamsIdSetup"][0]["id"]

    loanParamsAfter = bzx.getLoanParams([loanParamsId])[0]
    loanParamsAfter = dict(zip(list(loanParams.keys()), loanParamsAfter))
    print(loanParamsAfter)
    
    assert(loanParamsAfter["id"] != "0x0")
    assert(loanParamsAfter["active"])
    assert(loanParamsAfter["owner"] == accounts[0])
    assert(loanParamsAfter["loanToken"] == SUSD.address)

    with reverts("unauthorized owner"):
        bzx.disableLoanParams([loanParamsId], { "from": accounts[1] })
        
    bzx.disableLoanParams([loanParamsId], { "from": accounts[0] })
    assert(bzx.getLoanParams([loanParamsId])[0][0] != "0x0")

def test_setup_removeLoanOrder(Constants, bzx, accounts, SUSD, WETH):

    loanParams = {
        "id": "0x0",
        "active": False,
        "owner": Constants["ZERO_ADDRESS"],
        "loanToken": SUSD.address,
        "collateralToken": WETH.address,
        "initialMargin": Wei("50 ether"),
        "maintenanceMargin": Wei("15 ether"),
        "fixedLoanTerm": "2419200"
    }
    tx = bzx.setupLoanParams([list(loanParams.values())])

    loanParamsId = tx.events["LoanParamsIdSetup"][0]["id"]

    loanParamsAfter = bzx.getLoanParams([loanParamsId])[0]
    loanParamsAfter = dict(zip(list(loanParams.keys()), loanParamsAfter))
    print(loanParamsAfter)
    
    assert(loanParamsAfter["id"] != "0x0")
    assert(loanParamsAfter["active"])
    assert(loanParamsAfter["owner"] == accounts[0])
    assert(loanParamsAfter["loanToken"] == SUSD.address)

    with reverts("unauthorized owner"):
        bzx.disableLoanParams([loanParamsId], { "from": accounts[1] })
        
    bzx.disableLoanParams([loanParamsId], { "from": accounts[0] })
    assert(bzx.getLoanParams([loanParamsId])[0][0] != "0x0")