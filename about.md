### Introduction
tnbCrow is the first escrow application being built for thenewboston. We facilitate the users to escrow TNBC via various methods that they prefer.

### How it works
#### I want to Buy TNBC
- Go to `tnbcrow.com`
- Login/ Signup to the site. Provide your primary wallet address in the wallet section of your profile.
- Create a trade post filling every info for your request. `Your role will be buyer`
- Seller will come in and send you a trade request.
- Accept the trade request if both parties(you and seller) agree with the Terms and Condition.
- Pay the seller with the payment method that you agreed with.
- Verify that you have sent the payment method.
- Once the seller verifies the same, we will load coins into your primary wallet address.

#### I want to Sell TNBC
- Go to `tnbcrow.com`
- Login/ Signup to the site.
- Load coins into your tnbCrow account following the instructions provided.
- Create a trade post filling every info for your request. `You must have XXXX amount of coins into your wallet for creating XXXX coins trade request. Your role will be seller`
- Buyer will come in and send you a trade request.
- Accept the trade request if both parties(you and buyer) agree with the Terms and Condition.
- Wait for the payment from the buyer.
- Verify that you have recieved the payment.
- Once the buyer verifies the same, we will load coins into your buyers primary wallet address.

### Flow Image:
![Image of UserFlow](https://user-images.githubusercontent.com/55182298/111249983-aa637c00-8634-11eb-9e26-723abc92925a.png)

### User Balance Flow
#### Role - Seller
- User will load the coins into tnbCrow wallet. We will scan the chain with the memo and update the balance of the user.
- When the user is creating a trading post, they will need to have X coins loaded into their account before creating.
- Once they create a trading post, the balance of the user is deducted so as to stop them from creating another trading post with no coins into the wallet.
- If they cancel or delete the trading post, the balance gets added to their account.
- If the trade is completed, we'll send coins to the buyer's primary wallet address.
#### Role - Buyer
- The user will create a trade post with the number of coins that they want.
- The seller will need to have X coins loaded into their account before creating a trade request.
- Once they create a trade request, the balance of the user is deducted so as to stop them from creating another trading request with no coins into the wallet.
- If the buyer cancels or deletes the trading post or rejects a trade request, the balance gets added to the seller's account.
- If the trade is completed, we'll send coins to the buyer's primary wallet address.
