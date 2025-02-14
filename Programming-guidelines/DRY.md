# DRY (Don’t Repeat Yourself)

### Definition

**DRY** stands for **Don’t Repeat Yourself**. It’s a core software development principle stating that **every piece of knowledge or logic must have a single, unambiguous representation within a system**.

> “Duplication is the primary enemy of a well-designed system.” – Robert C. Martin

### Why It Matters

1. **Maintainability**: When code is duplicated in many places, updating or fixing it requires you to remember all occurrences—risking inconsistencies and bugs.  
2. **Readability**: Centralizing logic in one location avoids clutter and makes your code easier to understand.  
3. **Extensibility**: Systems with minimal duplication are easier to extend because you only update logic in one place when requirements change.  
4. **Consistency**: Having a single source of truth means less chance for conflicting implementations or data.

---

## Example in C#

Below is a hypothetical scenario demonstrating how to apply DRY to avoid code duplication.

### Before DRY: Repeated Code

```csharp
public class Invoice
{
    public decimal Amount { get; set; }
    public decimal Discount { get; set; }
    public decimal CalculateTotal()
    {
        // Suppose the discount is a percentage of the Amount
        // The discount should not exceed the Amount
        if (Discount > Amount)
        {
            Discount = Amount;
        }
        return Amount - Discount;
    }
}

public class Order
{
    public decimal Subtotal { get; set; }
    public decimal Discount { get; set; }
    public decimal CalculateTotal()
    {
        // Repeating the same discount logic
        if (Discount > Subtotal)
        {
            Discount = Subtotal;
        }
        return Subtotal - Discount;
    }
}
```

#### Observations

- **Invoice** and **Order** both have a similar concept of “subtract a discount, ensuring it doesn’t exceed the total amount.”  
- The logic (`if (Discount > Amount) Discount = Amount;`) is **duplicated** in both classes.  
- If we need to change how we calculate discount limits in the future, we’d have to **remember** to update it in multiple places—risking inconsistencies.

---

### After DRY: Centralized Logic

```csharp
public static class DiscountCalculator
{
    public static decimal CalculateTotalWithDiscount(decimal total, decimal discount)
    {
        if (discount > total)
        {
            discount = total;
        }
        return total - discount;
    }
}

public class Invoice
{
    public decimal Amount { get; set; }
    public decimal Discount { get; set; }

    public decimal CalculateTotal()
    {
        return DiscountCalculator.CalculateTotalWithDiscount(Amount, Discount);
    }
}

public class Order
{
    public decimal Subtotal { get; set; }
    public decimal Discount { get; set; }

    public decimal CalculateTotal()
    {
        return DiscountCalculator.CalculateTotalWithDiscount(Subtotal, Discount);
    }
}
```

#### Improvements

- **Shared Method**: We created a single `DiscountCalculator` utility class with a common method `CalculateTotalWithDiscount()`.  
- **No Duplication**: Both `Invoice` and `Order` classes now use the same discount calculation logic, preventing discrepancies.  
- **Single Source of Truth**: If the discount logic changes, we only have to modify it in **one place** (`DiscountCalculator`).

---

## Guidelines for Applying DRY

1. **Identify Common Patterns**: Look for duplicated code or logic across classes and modules.  
2. **Extract Shared Logic**: Move repeated code into a single function, utility class, or extension method.  
3. **Use Appropriate Abstraction**:  
   - If the logic is domain-specific, place it in a relevant service class or domain model.  
   - If the logic is more general, place it in a utility or helper class.  
4. **Refactor When Changes Arise**: When you make changes in one place, verify if the same change is needed in other areas.  
5. **Avoid Over-Abstraction**: Don’t blindly combine code that only looks similar but serves different purposes—balance DRY with clarity (sometimes code is *coincidentally* similar but not truly the same logic).

---

## Conclusion

**DRY** emphasizes the importance of **reducing duplication** in your codebase. By moving repeated logic to a **single** location, you improve maintainability, consistency, and clarity. A codebase that diligently applies DRY becomes **easier to update, test, and scale**, ultimately leading to more robust and reliable software.
