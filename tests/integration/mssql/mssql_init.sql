USE [master];
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[test](
	[PurchaseOrderID] [int] NOT NULL,
	[LineNumber] [smallint] NOT NULL,
	[UnitPrice] [money] NULL,
	[OrderQty] [smallint] NULL,
	[RejectedQty] [float] NULL,
	[DueDate] [datetime] NULL,
    [uniqueidentifier] [uniqueidentifier] NOT NULL DEFAULT NEWID(),
) ON [PRIMARY]
GO

INSERT INTO [master].[dbo].[test]
VALUES (1, 3, 1234.23, 3, 23.231, '2004-05-23T14:25:10', NEWID());
GO

