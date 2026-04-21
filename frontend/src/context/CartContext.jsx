import { createContext, useContext, useState, useEffect, useCallback } from "react";
import { authFetch, getAccessToken } from "../utils/auth";

const CartContext = createContext(null);

/** @param {{ children: React.ReactNode }} props */
export const CartProvider = ({ children }) => {
    const BASEURL = import.meta.env.VITE_DJANGO_BASE_URL;
    const [cartItems, setCartItems] = useState([]);
    const [total, setTotal] = useState(0);
    const [token, setToken] = useState(getAccessToken());
    const [authVersion, setAuthVersion] = useState(0);

    const refreshAuth = () => {
        setToken(getAccessToken());
        setAuthVersion(v => v + 1);
    };

    const isLoggedIn = !!token;

    //Fetch Cart form BE
    const fetchCart = useCallback(async () => {
        if (!getAccessToken()) {
            setCartItems([]);
            setTotal(0);
            return;
        }
        try {
            const res = await authFetch(`${BASEURL}/api/cart/`)
            if (res.status === 401 || res.status === 403) {
                clearCart();
                return;
            }
            const data = await res.json();
            setCartItems(data.items || []);
            setTotal(data.total || 0);
        } catch (error) {
            console.error("Error fetching cart:", error);
        }
    }, [BASEURL]);

    useEffect(() => {
        if (getAccessToken()) {
            fetchCart();
        } else {
            clearCart();
        }
    }, [authVersion, fetchCart]);

    /** @param {any} productId */
    const addToCart = async (productId) => {
        try{
            await authFetch(`${BASEURL}/api/cart/add/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ product_id: productId }),
            });
            fetchCart();
        } catch (error) {
            console.error("Error adding to cart:", error);
        }
    }

    /** @param {any} itemId */
    const removeFromCart = async (itemId) => {
        try{
            await authFetch(`${BASEURL}/api/cart/remove/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ item_id: itemId }),
            });
            fetchCart();
        } catch (error) {
            console.error("Error removing from cart:", error);
        }
    }

    /** 
     * @param {any} itemId 
     * @param {number} quantity 
     */
    const updateQuantity = async (itemId, quantity) => {
        if (quantity < 1){
            await removeFromCart(itemId);
            return;
        }
        try{
            await authFetch(`${BASEURL}/api/cart/update/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ item_id: itemId, quantity }),
            });
            fetchCart();
        } catch (error) {
            console.error("Error updating quantity:", error);
        }
    }

    const clearCart = () => {
        setCartItems([]);
        setTotal(0);
    }

    return (
        <CartContext.Provider
        value={{ cartItems,total, addToCart, removeFromCart, updateQuantity, clearCart, fetchCart, refreshAuth, isLoggedIn }}>
            {children}
        </CartContext.Provider>
    );
};

export const useCart = () => useContext(CartContext);